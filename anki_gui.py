import csv
import os
import re
import shutil
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk


APP_NAME = "AnkiHelperApp"
IMAGE_COLUMNS = ("Source", "Personal Notes", "Extra", "Missed Questions")


def app_folder():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def list_files(folder, pattern):
    return sorted(folder.glob(pattern), key=lambda path: path.name.lower())


def center_window(window, parent, width=None, height=None):
    window.update_idletasks()
    parent.update_idletasks()

    width = width or max(window.winfo_reqwidth(), 320)
    height = height or max(window.winfo_reqheight(), 160)
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    x = parent_x + max((parent_width - width) // 2, 0)
    y = parent_y + max((parent_height - height) // 2, 0)
    window.geometry(f"{width}x{height}+{x}+{y}")


def read_csv_rows(csv_path):
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames or [], list(reader)


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


def fix_back_field(text):
    if text is None:
        return ""

    text = str(text).strip()
    text = re.sub(r"\s+(U:)", r"<br>\1", text)
    text = re.sub(r"\s+(F:)", r"<br>\1", text)
    text = re.sub(r"\s+(I:)", r"<br>\1", text)
    text = re.sub(r"(?<!<b>)([UFIO]:)(?!</b>)", r"<b>\1</b>", text)
    return text


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


class AnkiGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.folder = app_folder()
        self.title(APP_NAME)
        self.geometry("640x720")
        self.minsize(560, 640)
        self.configure(bg="#1f1f1f")

        self.status_var = tk.StringVar(value=f"Pracovný priečinok: {self.folder}")
        self.counts_var = tk.StringVar()

        self._build_style()
        self._build_ui()
        self.refresh_counts()

    def _build_style(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("App.TFrame", background="#1f1f1f")
        self.style.configure("Title.TLabel", background="#1f1f1f", foreground="#f2f2f2", font=("Segoe UI", 24, "bold"))
        self.style.configure("Info.TLabel", background="#1f1f1f", foreground="#c8c8c8", font=("Segoe UI", 10))
        self.style.configure("Action.TButton", font=("Segoe UI", 13), padding=(16, 14))
        self.style.map("Action.TButton", background=[("active", "#3a3a3a")])

    def _build_ui(self):
        root = ttk.Frame(self, style="App.TFrame", padding=24)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text=APP_NAME, style="Title.TLabel").pack(pady=(4, 8))
        ttk.Label(root, textvariable=self.counts_var, style="Info.TLabel").pack(pady=(0, 18))

        actions = [
            ("Otvoriť tento priečinok", self.open_folder),
            ("Exportovať PDF do JPG", self.pdf_to_jpg),
            ("Pridať obrázkové tagy do CSV", self.add_images_to_csv),
            ("Kopírovať / presunúť JPG súbory", self.move_jpg_to_folder),
            ("Extrahovať TXT z PDF", self.extract_text_from_pdf),
            ("Vymazať strany z PDF", self.delete_pdf_pages),
            ("Premenovať PDF súbory", self.rename_pdf),
            ("Pridať tag do CSV", self.add_tags_to_csv),
            ("Opraviť stĺpec Back", self.fix_back_column),
        ]

        for label, command in actions:
            ttk.Button(root, text=label, style="Action.TButton", command=self.run_safe(command)).pack(fill="x", pady=6)

        ttk.Label(root, textvariable=self.status_var, style="Info.TLabel", wraplength=540).pack(side="bottom", pady=(18, 0))

    def run_safe(self, command):
        def wrapper():
            try:
                command()
                self.refresh_counts()
            except Exception as error:
                messagebox.showerror(APP_NAME, str(error), parent=self)
                self.set_status(f"Chyba: {error}")

        return wrapper

    def set_status(self, text):
        self.status_var.set(text)

    def refresh_counts(self):
        pdf_count = len(list_files(self.folder, "*.pdf"))
        csv_count = len(list_files(self.folder, "*.csv"))
        jpg_count = len(list_files(self.folder, "*.jpg")) + len(list_files(self.folder, "*.jpeg"))
        self.counts_var.set(f"{pdf_count} PDF   |   {csv_count} CSV   |   {jpg_count} JPG")

    def open_folder(self):
        os.startfile(self.folder)

    def choose_one_file(self, pattern, title):
        files = list_files(self.folder, pattern)
        if not files:
            messagebox.showinfo(APP_NAME, f"V tomto priečinku sa nenašli súbory {pattern}.", parent=self)
            return None
        return ChooseFilesDialog(self, title, files, multiple=False).result

    def choose_many_files(self, pattern, title):
        files = list_files(self.folder, pattern)
        if not files:
            messagebox.showinfo(APP_NAME, f"V tomto priečinku sa nenašli súbory {pattern}.", parent=self)
            return []
        return ChooseFilesDialog(self, title, files, multiple=True).result or []

    def ask_choice(self, title, choices):
        return ChoiceDialog(self, title, choices).result

    def ask_columns(self, fieldnames):
        available = [column for column in IMAGE_COLUMNS if column in fieldnames]
        if not available:
            messagebox.showinfo(
                APP_NAME,
                "Nenašli sa podporované stĺpce pre obrázky.\n\nPodporované stĺpce:\n" + "\n".join(IMAGE_COLUMNS),
                parent=self,
            )
            return []
        return CheckboxDialog(self, "Stĺpce na úpravu", available).result or []

    def ask_base_name(self):
        mode = self.ask_choice("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Kniha"])
        if mode is None:
            return None

        if mode == 0:
            subject = simpledialog.askstring(APP_NAME, "Skratka predmetu:", parent=self)
            if not subject:
                return None

            content_type = self.ask_choice("Typ materiálu", ["Cvičenie", "Prednáška"])
            if content_type is None:
                return None

            prefix = "C" if content_type == 0 else "P"
            number = simpledialog.askinteger(APP_NAME, f"Číslo {prefix}:", minvalue=0, parent=self)
            if number is None:
                return None
            return lambda pdf_path=None: f"{subject.strip()}_{prefix}_{number:02d}", mode

        book = simpledialog.askstring(APP_NAME, "Skratka/názov knihy:", parent=self)
        if not book:
            return None
        return lambda pdf_path=None: f"KNIHA_{book.strip()}", mode

    def pdf_to_jpg(self):
        pdfs = self.choose_many_files("*.pdf", "Vyber PDF súbory")
        if not pdfs:
            return

        mode = self.ask_choice("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Kniha"])
        if mode is None:
            return

        if mode == 0:
            subject = simpledialog.askstring(APP_NAME, "Skratka predmetu:", parent=self)
            if not subject:
                return
            content_type = self.ask_choice("Typ materiálu", ["Cvičenie", "Prednáška"])
            if content_type is None:
                return
            prefix = "C" if content_type == 0 else "P"
            number = simpledialog.askinteger(APP_NAME, f"Číslo {prefix}:", minvalue=0, parent=self)
            if number is None:
                return
            base_for_pdf = lambda pdf: f"{subject.strip()}_{prefix}_{number:02d}"
            dpi = None
        else:
            base_for_pdf = lambda pdf: f"KNIHA_{pdf.stem}"
            dpi = 300

        import fitz
        from PIL import Image

        exported = 0
        for pdf_path in pdfs:
            output_folder = self.folder / f"jpg_from_{pdf_path.stem}"
            output_folder.mkdir(exist_ok=True)
            document = fitz.open(pdf_path)
            try:
                for page_index in range(len(document)):
                    page = document.load_page(page_index)
                    pix = page.get_pixmap(dpi=dpi) if dpi else page.get_pixmap()
                    filename = f"{base_for_pdf(pdf_path)}_S_{page_index + 1:02d}.jpg"
                    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    image.save(output_folder / filename, quality=100)
                    exported += 1
            finally:
                document.close()

        messagebox.showinfo(APP_NAME, f"Exportovaných JPG súborov: {exported}", parent=self)
        self.set_status(f"Exportovaných JPG súborov: {exported}")

    def add_images_to_csv(self):
        csv_path = self.choose_one_file("*.csv", "Vyber CSV")
        if not csv_path:
            return

        fieldnames, rows = read_csv_rows(csv_path)
        columns = self.ask_columns(fieldnames)
        if not columns:
            return

        base_result = self.ask_base_name()
        if not base_result:
            return
        base_for_pdf, _mode = base_result
        base_name = base_for_pdf()

        changed = 0
        for row in rows:
            for column in columns:
                page = number_from_cell(row.get(column))
                if page is None:
                    continue
                row[column] = image_tag(f"{base_name}_S_{page:02d}.jpg")
                changed += 1

        output_path = csv_path.with_name(f"{csv_path.stem}_images.csv")
        write_csv_rows(output_path, fieldnames, rows)
        messagebox.showinfo(APP_NAME, f"Uložené: {output_path.name}\nUpravených buniek: {changed}", parent=self)
        self.set_status(f"Uložené: {output_path.name}")

    def move_jpg_to_folder(self):
        folders = [path for path in sorted(self.folder.iterdir(), key=lambda item: item.name.lower()) if path.is_dir()]
        if not folders:
            messagebox.showinfo(APP_NAME, "V tomto priečinku sa nenašli žiadne priečinky.", parent=self)
            return

        source = ChooseFilesDialog(self, "Vyber zdrojový priečinok", folders, multiple=False).result
        if not source:
            return

        destination = filedialog.askdirectory(parent=self, title="Vyber cieľový priečinok")
        if not destination:
            return

        action = self.ask_choice("Akcia", ["Kopírovať súbory", "Presunúť súbory"])
        if action is None:
            return

        destination = Path(destination)
        moved = 0
        for file_path in source.iterdir():
            if not file_path.is_file():
                continue
            target = destination / file_path.name
            if action == 0:
                shutil.copy2(file_path, target)
            else:
                shutil.move(str(file_path), str(target))
            moved += 1

        messagebox.showinfo(APP_NAME, f"Spracovaných súborov: {moved}", parent=self)
        self.set_status(f"Spracovaných súborov: {moved}")

    def extract_text_from_pdf(self):
        pdf_path = self.choose_one_file("*.pdf", "Vyber PDF")
        if not pdf_path:
            return

        mode = self.ask_choice("Typ textu", ["Prednáška s oddeľovačmi strán", "Kniha - vyčistený text"])
        if mode is None:
            return

        import fitz

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
                        page_text = page.get_text() or "[No extractable text]\n"
                        lines = [line for line in page_text.splitlines() if not omit_pattern.match(line)]
                        text_file.write("\n".join(lines) + "\n")
        finally:
            document.close()

        os.startfile(output_path)
        self.set_status(f"Uložené: {output_path.name}")

    def delete_pdf_pages(self):
        pdf_path = self.choose_one_file("*.pdf", "Vyber PDF")
        if not pdf_path:
            return

        import fitz

        document = fitz.open(pdf_path)
        page_count = document.page_count
        raw = simpledialog.askstring(
            APP_NAME,
            f"{pdf_path.name} má {page_count} strán.\nStrany na vymazanie, napr. 1,3,5-7:",
            parent=self,
        )
        if not raw:
            document.close()
            return

        try:
            pages_to_delete = parse_pages(raw, page_count)
        except ValueError as error:
            document.close()
            messagebox.showerror(APP_NAME, str(error), parent=self)
            return

        pages_to_keep = [index for index in range(page_count) if index not in pages_to_delete]
        if not pages_to_keep:
            document.close()
            messagebox.showerror(APP_NAME, "PDF nemôže ostať bez strán.", parent=self)
            return

        output_path = pdf_path.with_name(f"{pdf_path.stem}_modified.pdf")
        try:
            document.select(pages_to_keep)
            document.save(output_path)
        finally:
            document.close()

        messagebox.showinfo(APP_NAME, f"Uložené: {output_path.name}", parent=self)
        self.set_status(f"Uložené: {output_path.name}")

    def rename_pdf(self):
        pdf_path = self.choose_one_file("*.pdf", "Vyber PDF")
        if not pdf_path:
            return

        new_name = simpledialog.askstring(APP_NAME, f"Nový názov pre {pdf_path.name} bez .pdf:", parent=self)
        if not new_name:
            return

        output_path = pdf_path.with_name(f"{new_name.strip()}.pdf")
        if output_path.exists():
            messagebox.showerror(APP_NAME, f"{output_path.name} už existuje.", parent=self)
            return

        pdf_path.rename(output_path)
        messagebox.showinfo(APP_NAME, f"Premenované na: {output_path.name}", parent=self)
        self.set_status(f"Premenované na: {output_path.name}")

    def add_tags_to_csv(self):
        csv_files = self.choose_many_files("*.csv", "Vyber CSV súbory")
        if not csv_files:
            return

        tag = simpledialog.askstring(APP_NAME, "Tag, ktorý sa pridá tam, kde je Tags prázdne:", parent=self)
        if tag is None:
            return

        messages = []
        for csv_path in csv_files:
            fieldnames, rows = read_csv_rows(csv_path)
            if "Tags" not in fieldnames:
                messages.append(f"{csv_path.name}: chýba stĺpec Tags")
                continue

            changed = 0
            for row in rows:
                if not str(row.get("Tags", "")).strip():
                    row["Tags"] = tag
                    changed += 1

            output_path = csv_path.with_name(f"{csv_path.stem}_tagged.csv")
            write_csv_rows(output_path, fieldnames, rows)
            messages.append(f"{output_path.name}: upravených riadkov {changed}")

        messagebox.showinfo(APP_NAME, "\n".join(messages), parent=self)
        self.set_status("Tagy boli pridané.")

    def fix_back_column(self):
        csv_path = self.choose_one_file("*.csv", "Vyber CSV")
        if not csv_path:
            return

        fieldnames, rows = read_csv_rows(csv_path)
        if "Back" not in fieldnames:
            messagebox.showerror(APP_NAME, "Toto CSV nemá stĺpec Back.", parent=self)
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
        messagebox.showinfo(APP_NAME, f"Uložené: {output_path.name}\nUpravených riadkov: {changed}", parent=self)
        self.set_status(f"Uložené: {output_path.name}")


class ChooseFilesDialog(tk.Toplevel):
    def __init__(self, parent, title, paths, multiple):
        super().__init__(parent)
        self.withdraw()
        self.title(title)
        self.configure(bg="#252525")
        self.transient(parent)
        self.grab_set()
        self.result = [] if multiple else None
        self.paths = paths
        self.multiple = multiple

        tk.Label(self, text=title, bg="#252525", fg="#f2f2f2", font=("Segoe UI", 14, "bold")).pack(pady=(16, 8))
        selectmode = tk.MULTIPLE if multiple else tk.BROWSE
        self.listbox = tk.Listbox(self, selectmode=selectmode, font=("Segoe UI", 11), bg="#1f1f1f", fg="#f2f2f2")
        self.listbox.pack(fill="both", expand=True, padx=18, pady=8)

        for path in paths:
            self.listbox.insert(tk.END, path.name)

        buttons = tk.Frame(self, bg="#252525")
        buttons.pack(fill="x", padx=18, pady=(6, 16))
        ttk.Button(buttons, text="Zrušiť", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="OK", command=self.ok).pack(side="right")

        self.listbox.bind("<Double-Button-1>", lambda _event: self.ok())
        center_window(self, parent, 520, 380)
        self.deiconify()
        self.wait_window()

    def ok(self):
        selected = list(self.listbox.curselection())
        if not selected:
            return
        if self.multiple:
            self.result = [self.paths[index] for index in selected]
        else:
            self.result = self.paths[selected[0]]
        self.destroy()


class ChoiceDialog(tk.Toplevel):
    def __init__(self, parent, title, choices):
        super().__init__(parent)
        self.withdraw()
        self.title(title)
        self.configure(bg="#252525")
        self.transient(parent)
        self.grab_set()
        self.result = None

        tk.Label(self, text=title, bg="#252525", fg="#f2f2f2", font=("Segoe UI", 13, "bold")).pack(padx=18, pady=(16, 8))
        for index, choice in enumerate(choices):
            ttk.Button(self, text=choice, command=lambda i=index: self.choose(i)).pack(fill="x", padx=18, pady=5)
        ttk.Button(self, text="Zrušiť", command=self.destroy).pack(fill="x", padx=18, pady=(12, 16))

        center_window(self, parent)
        self.deiconify()
        self.wait_window()

    def choose(self, index):
        self.result = index
        self.destroy()


class CheckboxDialog(tk.Toplevel):
    def __init__(self, parent, title, options):
        super().__init__(parent)
        self.withdraw()
        self.title(title)
        self.configure(bg="#252525")
        self.transient(parent)
        self.grab_set()
        self.result = []
        self.vars = []

        tk.Label(self, text=title, bg="#252525", fg="#f2f2f2", font=("Segoe UI", 13, "bold")).pack(padx=18, pady=(16, 8))
        box = tk.Frame(self, bg="#252525")
        box.pack(fill="x", padx=18)

        for option in options:
            var = tk.BooleanVar(value=True)
            self.vars.append((option, var))
            tk.Checkbutton(
                box,
                text=option,
                variable=var,
                bg="#252525",
                fg="#f2f2f2",
                selectcolor="#1f1f1f",
                activebackground="#252525",
                activeforeground="#ffffff",
                font=("Segoe UI", 11),
            ).pack(anchor="w", pady=3)

        buttons = tk.Frame(self, bg="#252525")
        buttons.pack(fill="x", padx=18, pady=(12, 16))
        ttk.Button(buttons, text="Zrušiť", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="OK", command=self.ok).pack(side="right")

        center_window(self, parent)
        self.deiconify()
        self.wait_window()

    def ok(self):
        self.result = [option for option, var in self.vars if var.get()]
        self.destroy()


if __name__ == "__main__":
    AnkiGui().mainloop()
