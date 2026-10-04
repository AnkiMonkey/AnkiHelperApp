"""Konzolová verzia AnkiHelperApp – rovnaká logika ako GUI (balík core/)."""

import sys
from pathlib import Path

from core import DOCUMENT_DPI, IMAGE_COLUMNS, LECTURE_DPI
from core import fields, media, naming, pdf, tables
from core.pages import parse_pages
from core.system import app_folder, list_files, list_subfolders, list_tables, open_path


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


def ask_int(prompt, minimum=None, maximum=None, default=None):
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
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


def ask_yes(prompt):
    return ask(f"{prompt} a/N: ", required=False).lower() in ("a", "y")


def choose_one(paths, title):
    if not paths:
        print(f"Nenašli sa súbory pre: {title}")
        return None

    print(f"\n{title}:")
    for index, path in enumerate(paths, start=1):
        print(f"{index}. {path.name}")

    choice = ask_int("Vyber číslo: ", 1, len(paths))
    return paths[choice - 1]


def choose_many(paths, title):
    if not paths:
        print(f"Nenašli sa súbory pre: {title}")
        return []

    print(f"\n{title}:")
    for index, path in enumerate(paths, start=1):
        print(f"{index}. {path.name}")

    raw = ask("Vyber čísla (napr. 1,3 alebo 2-5): ")
    try:
        indexes = sorted(parse_pages(raw, len(paths)))
    except ValueError as error:
        print(error)
        return []
    return [paths[index] for index in indexes]


def choose_from_menu(title, options):
    print(f"\n{title}:")
    for index, label in enumerate(options, start=1):
        print(f"{index}. {label}")
    return ask_int("Vyber možnosť: ", 1, len(options)) - 1


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


def read_chosen_table(path):
    sheet = None
    if tables.is_xlsx(path):
        sheets = tables.xlsx_sheets(path)
        sheet = sheets[choose_from_menu(f"Ktorý list z {path.name}?", sheets)] if len(sheets) > 1 else sheets[0]
    return tables.read_any(path, sheet)


def ask_lecture_header():
    subject = naming.validate_base(ask("Skratka predmetu: "))
    labels = list(naming.LECTURE_PREFIXES)
    prefix = naming.LECTURE_PREFIXES[labels[choose_from_menu("Typ materiálu", labels)]]
    return subject, prefix


# ---------------------------------------------------------------- akcie


def open_folder(folder):
    open_path(folder)


def pdf_to_jpg(folder):
    pdfs = choose_many(list_files(folder, "*.pdf"), "PDF súbory")
    if not pdfs:
        return

    mode = choose_from_menu("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Dokument (vypracovanie / kniha)"])
    jobs = []
    if mode == 0:
        subject, prefix = ask_lecture_header()
        suggestion = None
        for pdf_path in pdfs:
            hint = f" [{suggestion}]" if suggestion is not None else ""
            label = f"Číslo {prefix} pre {pdf_path.name}{hint}: " if len(pdfs) > 1 else f"Číslo {prefix}: "
            number = ask_int(label, 0, default=suggestion)
            jobs.append((pdf_path, naming.lecture_base(subject, prefix, number), LECTURE_DPI))
            suggestion = number + 1
    else:
        jobs = [(pdf_path, naming.validate_base(pdf_path.stem), DOCUMENT_DPI) for pdf_path in pdfs]

    duplicates = naming.find_duplicate_bases(base for _, base, _ in jobs)
    if duplicates:
        print("Rovnaký názov pre viac PDF – obrázky by sa prepísali:", ", ".join(duplicates))
        return

    for pdf_path, base, dpi in jobs:
        print(f"\nKonvertujem {pdf_path.name} -> {base}_S_##.jpg")

        def progress(done, total):
            print(f"\r  strana {done}/{total}", end="", flush=True)

        files = pdf.export_jpg(pdf_path, folder / f"jpg_{base}", base, dpi, progress=progress)
        print(f"\n  Uložené: {len(files)} JPG")


def add_images_to_table(folder):
    table_path = choose_one(list_tables(folder), "CSV/TSV/XLSX súbory")
    if not table_path:
        return

    fieldnames, rows = read_chosen_table(table_path)
    columns = ask_columns(fieldnames)
    if not columns:
        return

    mode = choose_from_menu("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Dokument (vypracovanie / kniha)"])
    if mode == 0:
        subject, prefix = ask_lecture_header()
        number = ask_int(f"Číslo {prefix}: ", 0)
        base = naming.lecture_base(subject, prefix, number)
    else:
        base = naming.validate_base(ask("Názov dokumentu/PDF bez .pdf: "))

    changed, skipped = fields.add_images_to_rows(rows, columns, base)
    output = tables.output_path(table_path, "images")
    tables.write_anki_tsv(output, fieldnames, rows)
    print(f"\nUložené: {output.name}")
    print(f"Upravených buniek: {changed}")
    if skipped:
        print(f"⚠ Nečitateľné bunky (ostali bez zmeny): {len(skipped)}")
        for row, column, value in skipped[:20]:
            print(f"  riadok {row}, {column}: {value[:50]}")


def move_images_to_folder(folder):
    source = choose_one(list_subfolders(folder), "Zdrojové priečinky")
    if not source:
        return

    files = media.image_files(source)
    if not files:
        print("V zdrojovom priečinku nie sú žiadne obrázky.")
        return

    destination = Path(ask("Cesta k cieľovému priečinku (napr. collection.media): ").strip('"')).expanduser()
    move = choose_from_menu("Akcia", ["Kopírovať súbory", "Presunúť súbory"]) == 1

    plan = media.plan_transfer(files, destination)
    print("\n" + media.describe_plan(plan))
    overwrite = True
    if plan.changed:
        overwrite = ask_yes("\nPrepísať súbory s iným obsahom?")

    done = media.execute_transfer(plan, move=move, overwrite_changed=overwrite)
    print(f"\nSpracovaných: {done}")


def extract_text_from_pdf(folder):
    pdf_path = choose_one(list_files(folder, "*.pdf"), "PDF súbory")
    if not pdf_path:
        return

    mode = choose_from_menu("Typ textu", ["Prednáška s oddeľovačmi strán", "Dokument - vyčistený text"])
    output = pdf.extract_text(pdf_path, with_page_separators=(mode == 0))
    print(f"Uložené: {output.name}")
    open_path(output)


def delete_pdf_pages(folder):
    pdf_path = choose_one(list_files(folder, "*.pdf"), "PDF súbory")
    if not pdf_path:
        return

    count = pdf.page_count(pdf_path)
    print(f"{pdf_path.name} má {count} strán.")
    raw = ask("Strany na vymazanie, napr. 1,3,5-7: ")
    try:
        output = pdf.delete_pages(pdf_path, parse_pages(raw, count))
    except ValueError as error:
        print(error)
        return
    print(f"Uložené: {output.name}")


def rename_pdf(folder):
    while True:
        pdf_path = choose_one(list_files(folder, "*.pdf"), "PDF súbory")
        if not pdf_path:
            return

        new_name = ask(f"Nový názov pre {pdf_path.name} bez .pdf: ")
        try:
            target = pdf.rename(pdf_path, naming.validate_base(new_name))
        except (ValueError, FileExistsError) as error:
            print(error)
            continue
        print(f"Premenované na: {target.name}")

        if not ask_yes("Premenovať ďalšie PDF?"):
            return


def add_tags_to_table(folder):
    selected = choose_many(list_tables(folder), "CSV/TSV/XLSX súbory")
    if not selected:
        return

    tag = ask("Tag, ktorý sa pridá tam, kde je Tags prázdne: ")
    for table_path in selected:
        fieldnames, rows = read_chosen_table(table_path)
        if "Tags" not in fieldnames:
            print(f"{table_path.name}: chýba stĺpec Tags")
            continue
        changed = fields.fill_empty_tags(rows, tag)
        output = tables.output_path(table_path, "tagged")
        tables.write_anki_tsv(output, fieldnames, rows)
        print(f"{table_path.name}: uložené {output.name}, upravených riadkov {changed}")


def fix_back_column(folder):
    table_path = choose_one(list_tables(folder), "CSV/TSV/XLSX súbory")
    if not table_path:
        return

    fieldnames, rows = read_chosen_table(table_path)
    if "Back" not in fieldnames:
        print("Tento súbor nemá stĺpec Back.")
        print("Nájdené stĺpce:", ", ".join(fieldnames))
        return

    changed = fields.fix_back_rows(rows)
    output = tables.output_path(table_path, "fixed")
    tables.write_anki_tsv(output, fieldnames, rows)
    print(f"\nUložené: {output.name}")
    print(f"Upravených riadkov: {changed}")
    print("Import do Anki: File → Import → tento .tsv (HTML a stĺpce sa nastavia samé).")


MENU = [
    ("Otvoriť tento priečinok", open_folder),
    ("Exportovať PDF do JPG", pdf_to_jpg),
    ("Pridať obrázkové tagy (CSV/TSV/XLSX)", add_images_to_table),
    ("Kopírovať / presunúť obrázky", move_images_to_folder),
    ("Extrahovať TXT z PDF", extract_text_from_pdf),
    ("Vymazať strany z PDF", delete_pdf_pages),
    ("Premenovať PDF súbory", rename_pdf),
    ("Pridať tag (CSV/TSV/XLSX)", add_tags_to_table),
    ("Opraviť stĺpec Back", fix_back_column),
]


def main():
    configure_console_encoding()
    folder = app_folder()

    while True:
        print("\nAnki Helper")
        print(f"Pracovný priečinok: {folder}")
        for index, (label, _action) in enumerate(MENU, start=1):
            print(f"{index}. {label}")
        print(f"{len(MENU) + 1}. Koniec")

        choice = ask_int("Vyber možnosť: ", 1, len(MENU) + 1)
        if choice == len(MENU) + 1:
            print("Koniec.")
            return

        try:
            MENU[choice - 1][1](folder)
        except Exception as error:
            print(f"\nChyba: {error}")
        pause()


if __name__ == "__main__":
    main()
