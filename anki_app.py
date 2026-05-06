import csv
import os
import re
import shutil
import sys
from pathlib import Path


APP_NAME = "Anki Helper"
IMAGE_COLUMNS = ("Source", "Personal Notes", "Extra", "Missed Questions")


def app_folder():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def configure_console_encoding():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream and hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def pause():
    input("\nStlač Enter pre pokračovanie...")


def ask(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("Zadaj hodnotu.")


def ask_int(prompt, minimum=None, maximum=None):
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Zadaj číslo.")
            continue

        number = int(value)
        if minimum is not None and number < minimum:
            print(f"Zadaj aspoň {minimum}.")
            continue
        if maximum is not None and number > maximum:
            print(f"Zadaj najviac {maximum}.")
            continue
        return number


def list_files(folder, pattern):
    return sorted(folder.glob(pattern), key=lambda path: path.name.lower())


def choose_one(paths, title):
    if not paths:
        print(f"Nenašli sa súbory pre: {title}")
        return None

    print(f"\n{title}:")
    for index, path in enumerate(paths, start=1):
        print(f"{index}. {path.name}")

    choice = ask_int("Vyber číslo súboru: ", 1, len(paths))
    return paths[choice - 1]


def choose_many(paths, title):
    if not paths:
        print(f"Nenašli sa súbory pre: {title}")
        return []

    print(f"\n{title}:")
    for index, path in enumerate(paths, start=1):
        print(f"{index}. {path.name}")

    raw = ask("Vyber čísla oddelené čiarkou: ")
    selected = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            index = int(part)
            if 1 <= index <= len(paths):
                selected.append(paths[index - 1])
    return selected


def choose_from_menu(title, options):
    print(f"\n{title}:")
    for index, label in enumerate(options, start=1):
        print(f"{index}. {label}")
    return ask_int("Vyber možnosť: ", 1, len(options)) - 1


def read_csv_rows(csv_path):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    return fieldnames, rows


def write_csv_rows(csv_path, fieldnames, rows):
    with csv_path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def number_from_cell(value):
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    try:
        return int(text)
    except ValueError:
        try:
            number = float(text)
        except ValueError:
            return None
        if number.is_integer():
            return int(number)
    return None


def image_tag(filename, width=450):
    return f'<img src="{filename}" data-editor-shrink="false" width="{width}">'


def ask_columns(fieldnames):
    available = [column for column in IMAGE_COLUMNS if column in fieldnames]
    if not available:
        print("Nenašli sa podporované stĺpce pre obrázky.")
        print("Podporované stĺpce:", ", ".join(IMAGE_COLUMNS))
        return []

    options = available + ["Všetky"]
    choice = choose_from_menu("Stĺpce na úpravu", options)
    if choice == len(options) - 1:
        return available
    return [available[choice]]


def add_images_to_csv(folder):
    csv_path = choose_one(list_files(folder, "*.csv"), "CSV súbory")
    if not csv_path:
        return

    mode = choose_from_menu("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Kniha"])
    fieldnames, rows = read_csv_rows(csv_path)
    columns = ask_columns(fieldnames)
    if not columns:
        return

    changed = 0

    if mode == 0:
        subject = ask("Skratka predmetu: ")
        content_type = choose_from_menu("Typ materiálu", ["Cvičenie", "Prednáška"])
        prefix = "C" if content_type == 0 else "P"
        number = ask_int(f"Číslo {prefix}: ", 0)
        base_name = f"{subject}_{prefix}_{number:02d}"
    else:
        book = ask("Skratka/názov knihy: ")
        base_name = f"KNIHA_{book}"

    for row in rows:
        for column in columns:
            page = number_from_cell(row.get(column))
            if page is None:
                continue
            filename = f"{base_name}_S_{page:02d}.jpg"
            row[column] = image_tag(filename)
            changed += 1

    output_path = csv_path.with_name(f"{csv_path.stem}_images.csv")
    write_csv_rows(output_path, fieldnames, rows)
    print(f"\nUložené: {output_path.name}")
    print(f"Upravených buniek: {changed}")


def add_tags_to_csv(folder):
    selected = choose_many(list_files(folder, "*.csv"), "CSV súbory")
    if not selected:
        print("Neboli vybrané platné CSV súbory.")
        return

    tag = ask("Tag, ktorý sa pridá tam, kde je Tags prázdne: ")
    for csv_path in selected:
        fieldnames, rows = read_csv_rows(csv_path)
        if "Tags" not in fieldnames:
            print(f"{csv_path.name}: chýba stĺpec Tags")
            continue

        changed = 0
        for row in rows:
            if not str(row.get("Tags", "")).strip():
                row["Tags"] = tag
                changed += 1

        output_path = csv_path.with_name(f"{csv_path.stem}_tagged.csv")
        write_csv_rows(output_path, fieldnames, rows)
        print(f"{csv_path.name}: uložené {output_path.name}, upravených riadkov {changed}")


def fix_back_field(text):
    if text is None:
        return ""

    text = str(text).strip()
    text = re.sub(r"\s+(U:)", r"<br>\1", text)
    text = re.sub(r"\s+(F:)", r"<br>\1", text)
    text = re.sub(r"\s+(I:)", r"<br>\1", text)
    text = re.sub(r"(?<!<b>)([UFIO]:)(?!</b>)", r"<b>\1</b>", text)
    return text


def fix_back_column(folder):
    csv_path = choose_one(list_files(folder, "*.csv"), "CSV súbory")
    if not csv_path:
        return

    fieldnames, rows = read_csv_rows(csv_path)
    if "Back" not in fieldnames:
        print("Toto CSV nemá stĺpec Back.")
        print("Nájdené stĺpce:", ", ".join(fieldnames))
        return

    changed = 0
    for row in rows:
        old_value = row.get("Back", "")
        new_value = fix_back_field(old_value)
        if old_value != new_value:
            changed += 1
        row["Back"] = new_value

    output_path = csv_path.with_name(f"{csv_path.stem}_fixed.csv")
    write_csv_rows(output_path, fieldnames, rows)
    print(f"\nUložené: {output_path.name}")
    print(f"Upravených riadkov: {changed}")
    print("Pri importe do Anki zapni HTML vo fieldoch.")


def pdf_to_jpg(folder):
    pdfs = choose_many(list_files(folder, "*.pdf"), "PDF súbory")
    if not pdfs:
        print("Neboli vybrané platné PDF súbory.")
        return

    mode = choose_from_menu("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Kniha"])
    if mode == 0:
        subject = ask("Skratka predmetu: ")
        content_type = choose_from_menu("Typ materiálu", ["Cvičenie", "Prednáška"])
        prefix = "C" if content_type == 0 else "P"
        number = ask_int(f"Číslo {prefix}: ", 0)
        base_for_pdf = lambda pdf: f"{subject}_{prefix}_{number:02d}"
        dpi = None
    else:
        base_for_pdf = lambda pdf: f"KNIHA_{pdf.stem}"
        dpi = 300

    try:
        import fitz
        from PIL import Image
    except ImportError as error:
        print(f"Chýba knižnica: {error}")
        return

    for pdf_path in pdfs:
        output_folder = folder / f"jpg_from_{pdf_path.stem}"
        output_folder.mkdir(exist_ok=True)
        print(f"\nKonvertujem {pdf_path.name}...")

        document = fitz.open(pdf_path)
        try:
            for page_index in range(len(document)):
                page = document.load_page(page_index)
                pix = page.get_pixmap(dpi=dpi) if dpi else page.get_pixmap()
                filename = f"{base_for_pdf(pdf_path)}_S_{page_index + 1:02d}.jpg"
                output_path = output_folder / filename
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                image.save(output_path, quality=100)
                print(f"Uložené: {output_path.name}")
        finally:
            document.close()


def extract_text_from_pdf(folder):
    pdf_path = choose_one(list_files(folder, "*.pdf"), "PDF súbory")
    if not pdf_path:
        return

    mode = choose_from_menu("Typ textu", ["Prednáška s oddeľovačmi strán", "Kniha - vyčistený text"])

    try:
        import fitz
    except ImportError as error:
        print(f"Chýba knižnica: {error}")
        return

    output_path = pdf_path.with_suffix(".txt")
    document = fitz.open(pdf_path)
    try:
        with output_path.open("w", encoding="utf-8") as text_file:
            if mode == 0:
                text_file.write(f"Toto je prepis z {pdf_path.stem}\n\n")
                for index, page in enumerate(document, start=1):
                    text_file.write("\n" + "-" * 19 + f"\nToto je strana {index}\n\n")
                    text_file.write(page.get_text() or "")
            else:
                omit_pattern = re.compile(r"Zoznam ot.+ / \d+\. strana")
                for page in document:
                    page_text = page.get_text() or "[Žiadny extrahovateľný text]\n"
                    lines = [line for line in page_text.splitlines() if not omit_pattern.match(line)]
                    text_file.write("\n".join(lines) + "\n")
    finally:
        document.close()

    print(f"Uložené: {output_path.name}")
    if os.name == "nt":
        os.startfile(output_path)


def parse_pages(raw, page_count):
    pages = set()
    try:
        for part in raw.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                start_text, end_text = part.split("-", 1)
                start = int(start_text.strip())
                end = int(end_text.strip())
                if start > end:
                    start, end = end, start
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
    except ValueError:
        raise ValueError("Použi čísla strán ako 1,3,5-7.")

    if not pages:
        raise ValueError("Neboli vybrané žiadne strany.")

    invalid = [page for page in pages if page < 1 or page > page_count]
    if invalid:
        raise ValueError(f"Neplatné číslo strany: {invalid}")
    return {page - 1 for page in pages}


def delete_pdf_pages(folder):
    pdf_path = choose_one(list_files(folder, "*.pdf"), "PDF súbory")
    if not pdf_path:
        return

    try:
        import fitz
    except ImportError as error:
        print(f"Chýba knižnica: {error}")
        return

    document = fitz.open(pdf_path)
    page_count = document.page_count
    print(f"{pdf_path.name} má {page_count} strán.")

    raw = ask("Strany na vymazanie, napr. 1,3,5-7: ")
    try:
        pages_to_delete = parse_pages(raw, page_count)
    except ValueError as error:
        print(error)
        document.close()
        return

    pages_to_keep = [index for index in range(page_count) if index not in pages_to_delete]
    if not pages_to_keep:
        print("PDF nemôže ostať bez strán.")
        document.close()
        return

    output_path = pdf_path.with_name(f"{pdf_path.stem}_modified.pdf")
    try:
        document.select(pages_to_keep)
        document.save(output_path)
        print(f"Uložené: {output_path.name}")
    finally:
        document.close()


def rename_pdf(folder):
    while True:
        pdf_path = choose_one(list_files(folder, "*.pdf"), "PDF súbory")
        if not pdf_path:
            return

        new_name = ask(f"Nový názov pre {pdf_path.name} bez .pdf: ")
        output_path = pdf_path.with_name(f"{new_name}.pdf")
        if output_path.exists():
            print(f"{output_path.name} už existuje.")
            continue

        pdf_path.rename(output_path)
        print(f"Premenované na: {output_path.name}")

        again = ask("Premenovať ďalšie PDF? a/N: ", required=False).lower()
        if again not in ("a", "y"):
            return


def open_folder(folder):
    os.startfile(folder)


def move_jpg_to_folder(folder):
    folders = [path for path in sorted(folder.iterdir(), key=lambda item: item.name.lower()) if path.is_dir()]
    source_folder = choose_one(folders, "Zdrojové priečinky")
    if not source_folder:
        return

    destination_text = ask("Cesta k cieľovému priečinku: ")
    destination = Path(destination_text).expanduser()
    destination.mkdir(parents=True, exist_ok=True)

    mode = choose_from_menu("Akcia", ["Kopírovať súbory", "Presunúť súbory"])
    files = [path for path in source_folder.iterdir() if path.is_file()]
    if not files:
        print("V zdrojovom priečinku sa nenašli žiadne súbory.")
        return

    for file_path in files:
        target = destination / file_path.name
        if mode == 0:
            shutil.copy2(file_path, target)
            print(f"Skopírované: {file_path.name}")
        else:
            shutil.move(str(file_path), str(target))
            print(f"Presunuté: {file_path.name}")


def run_option(folder, option):
    actions = {
        1: open_folder,
        2: pdf_to_jpg,
        3: add_images_to_csv,
        4: move_jpg_to_folder,
        5: extract_text_from_pdf,
        6: delete_pdf_pages,
        7: rename_pdf,
        8: add_tags_to_csv,
        9: fix_back_column,
    }
    actions[option](folder)


def main():
    configure_console_encoding()
    folder = app_folder()

    while True:
        print(f"\n{APP_NAME}")
        print(f"Pracovný priečinok: {folder}")
        print("1. Otvoriť tento priečinok")
        print("2. Exportovať PDF do JPG")
        print("3. Pridať obrázkové tagy do CSV")
        print("4. Kopírovať / presunúť JPG súbory")
        print("5. Extrahovať TXT z PDF")
        print("6. Vymazať strany z PDF")
        print("7. Premenovať PDF súbory")
        print("8. Pridať tag do CSV")
        print("9. Opraviť stĺpec Back")
        print("10. Koniec")

        choice = ask_int("Vyber možnosť: ", 1, 10)
        if choice == 10:
            print("Koniec.")
            return

        run_option(folder, choice)
        pause()


if __name__ == "__main__":
    main()
