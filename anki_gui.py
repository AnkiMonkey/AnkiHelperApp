import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from core import APP_NAME, DOCUMENT_DPI, IMAGE_COLUMNS, LECTURE_DPI
from core import fields, media, naming, pdf, tables
from core.pages import parse_pages
from core.system import app_folder, list_files, list_subfolders, list_tables, open_path


BG = "#1f1f1f"
BG_DIALOG = "#252525"
FG = "#f2f2f2"
FG_MUTED = "#c8c8c8"


def center_window(window, parent, width=None, height=None):
    window.update_idletasks()
    parent.update_idletasks()

    width = width or max(window.winfo_reqwidth(), 320)
    height = height or max(window.winfo_reqheight(), 160)
    x = parent.winfo_rootx() + max((parent.winfo_width() - width) // 2, 0)
    y = parent.winfo_rooty() + max((parent.winfo_height() - height) // 2, 0)
    window.geometry(f"{width}x{height}+{x}+{y}")


class AnkiGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.folder = app_folder()
        self.title(APP_NAME)
        self.geometry("640x780")
        self.minsize(560, 700)
        self.configure(bg=BG)

        self.status_var = tk.StringVar(value=f"Pracovný priečinok: {self.folder}")
        self.counts_var = tk.StringVar()
        self.buttons = []
        self._queue = queue.Queue()
        self._busy = False

        self._build_style()
        self._build_ui()
        self.refresh_counts()

    # ------------------------------------------------------------------ UI

    def _build_style(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("App.TFrame", background=BG)
        self.style.configure("Title.TLabel", background=BG, foreground=FG, font=("Segoe UI", 24, "bold"))
        self.style.configure("Info.TLabel", background=BG, foreground=FG_MUTED, font=("Segoe UI", 10))
        self.style.configure("Action.TButton", font=("Segoe UI", 13), padding=(16, 12))
        self.style.map("Action.TButton", background=[("active", "#3a3a3a")])
        self.style.configure("App.Horizontal.TProgressbar", troughcolor="#2b2b2b", background="#4a90e2")

    def _build_ui(self):
        root = ttk.Frame(self, style="App.TFrame", padding=24)
        root.pack(fill="both", expand=True)

        ttk.Label(root, text=APP_NAME, style="Title.TLabel").pack(pady=(4, 8))
        ttk.Label(root, textvariable=self.counts_var, style="Info.TLabel").pack(pady=(0, 14))

        actions = [
            ("Otvoriť tento priečinok", self.open_folder),
            ("Exportovať PDF do JPG", self.pdf_to_jpg),
            ("Pridať obrázkové tagy (CSV/TSV/XLSX)", self.add_images_to_table),
            ("Kopírovať / presunúť obrázky", self.move_images_to_folder),
            ("Extrahovať TXT z PDF", self.extract_text_from_pdf),
            ("Vymazať strany z PDF", self.delete_pdf_pages),
            ("Premenovať PDF súbory", self.rename_pdf),
            ("Pridať tag (CSV/TSV/XLSX)", self.add_tags_to_table),
            ("Opraviť stĺpec Back", self.fix_back_column),
        ]

        for label, command in actions:
            button = ttk.Button(root, text=label, style="Action.TButton", command=self.run_safe(command))
            button.pack(fill="x", pady=5)
            self.buttons.append(button)

        ttk.Label(root, textvariable=self.status_var, style="Info.TLabel", wraplength=560).pack(side="bottom", pady=(10, 0))
        self.progress = ttk.Progressbar(root, mode="determinate", style="App.Horizontal.TProgressbar")
        self.progress.pack(side="bottom", fill="x", pady=(14, 0))

    def run_safe(self, command):
        def wrapper():
            if self._busy:
                return
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
        table_count = len(list_tables(self.folder))
        jpg_count = len(list_files(self.folder, "*.jpg")) + len(list_files(self.folder, "*.jpeg"))
        self.counts_var.set(f"{pdf_count} PDF   |   {table_count} CSV/TSV/XLSX   |   {jpg_count} JPG")

    # ------------------------------------------------- práca na pozadí

    def run_in_background(self, work, on_done):
        """work(report) beží vo vlákne; report(done, total, text) aktualizuje progress bar."""
        self._busy = True
        for button in self.buttons:
            button.state(["disabled"])
        self.progress["value"] = 0

        def report(done, total, text=""):
            self._queue.put(("progress", done, total, text))

        def target():
            try:
                result = work(report)
                self._queue.put(("done", result))
            except Exception as error:  # chyba vo vlákne -> späť do GUI
                self._queue.put(("error", error))

        threading.Thread(target=target, daemon=True).start()
        self.after(100, self._poll_queue, on_done)

    def _poll_queue(self, on_done):
        try:
            while True:
                message = self._queue.get_nowait()
                kind = message[0]
                if kind == "progress":
                    _, done, total, text = message
                    self.progress["maximum"] = max(total, 1)
                    self.progress["value"] = done
                    if text:
                        self.set_status(text)
                else:
                    self._finish_background()
                    if kind == "done":
                        on_done(message[1])
                    else:
                        messagebox.showerror(APP_NAME, str(message[1]), parent=self)
                        self.set_status(f"Chyba: {message[1]}")
                    self.refresh_counts()
                    return
        except queue.Empty:
            pass
        self.after(100, self._poll_queue, on_done)

    def _finish_background(self):
        self._busy = False
        for button in self.buttons:
            button.state(["!disabled"])

    # ----------------------------------------------------- dialógy

    def choose_one(self, paths, title, empty_message):
        if not paths:
            messagebox.showinfo(APP_NAME, empty_message, parent=self)
            return None
        return ChooseFilesDialog(self, title, paths, multiple=False).result

    def choose_many(self, paths, title, empty_message):
        if not paths:
            messagebox.showinfo(APP_NAME, empty_message, parent=self)
            return []
        return ChooseFilesDialog(self, title, paths, multiple=True).result or []

    def choose_pdf(self, many=False):
        files = list_files(self.folder, "*.pdf")
        message = "V tomto priečinku sa nenašli PDF súbory."
        if many:
            return self.choose_many(files, "Vyber PDF súbory", message)
        return self.choose_one(files, "Vyber PDF", message)

    def choose_table(self, many=False):
        files = list_tables(self.folder)
        message = "V tomto priečinku sa nenašli CSV, TSV ani XLSX súbory."
        if many:
            return self.choose_many(files, "Vyber CSV/TSV/XLSX súbory", message)
        return self.choose_one(files, "Vyber CSV/TSV/XLSX", message)

    def read_chosen_table(self, path):
        """Pri XLSX s viacerými listami sa spýta, ktorý list (ALL-LECTURES je prvý). None = zrušené."""
        sheet = None
        if tables.is_xlsx(path):
            sheets = tables.xlsx_sheets(path)
            if len(sheets) > 1:
                labels = [f"{sheets[0]}  (odporúčaný)"] + sheets[1:] if "ALL-LECTURES" in sheets[0].upper() else sheets
                choice = self.ask_choice(f"Ktorý list z {path.name}?", labels)
                if choice is None:
                    return None
                sheet = sheets[choice]
            else:
                sheet = sheets[0]
        return tables.read_any(path, sheet)

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

    def ask_lecture_header(self):
        """Spýta sa na predmet a typ (C/P). Vráti (subject, prefix) alebo None."""
        subject = simpledialog.askstring(APP_NAME, "Skratka predmetu:", parent=self)
        if not subject or not subject.strip():
            return None
        naming.validate_base(subject)
        labels = list(naming.LECTURE_PREFIXES)
        content_type = self.ask_choice("Typ materiálu", labels)
        if content_type is None:
            return None
        return subject.strip(), naming.LECTURE_PREFIXES[labels[content_type]]

    def ask_number(self, prefix, pdf_name=None, initial=None):
        prompt = f"Číslo {prefix}:" if not pdf_name else f"Číslo {prefix} pre\n{pdf_name}:"
        return simpledialog.askinteger(APP_NAME, prompt, minvalue=0, initialvalue=initial, parent=self)

    # ------------------------------------------------------ akcie

    def open_folder(self):
        open_path(self.folder)

    def pdf_to_jpg(self):
        pdfs = self.choose_pdf(many=True)
        if not pdfs:
            return

        mode = self.ask_choice("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Dokument (vypracovanie / kniha)"])
        if mode is None:
            return

        jobs = []  # (pdf_path, base, dpi)
        if mode == 0:
            header = self.ask_lecture_header()
            if not header:
                return
            subject, prefix = header
            # Každé PDF dostane vlastné číslo – inak by sa obrázky prepisovali.
            suggestion = None
            for pdf_path in pdfs:
                number = self.ask_number(prefix, pdf_path.name if len(pdfs) > 1 else None, suggestion)
                if number is None:
                    return
                jobs.append((pdf_path, naming.lecture_base(subject, prefix, number), LECTURE_DPI))
                suggestion = number + 1
        else:
            jobs = [(pdf_path, naming.validate_base(pdf_path.stem), DOCUMENT_DPI) for pdf_path in pdfs]

        duplicates = naming.find_duplicate_bases(base for _, base, _ in jobs)
        if duplicates:
            raise ValueError(
                "Rovnaký názov pre viac PDF – obrázky by sa navzájom prepísali:\n" + "\n".join(duplicates)
            )

        folder = self.folder

        def work(report):
            exported = 0
            for index, (pdf_path, base, dpi) in enumerate(jobs, start=1):
                label = f"[{index}/{len(jobs)}] {pdf_path.name}"
                files = pdf.export_jpg(
                    pdf_path,
                    folder / f"jpg_{base}",
                    base,
                    dpi,
                    progress=lambda done, total, label=label: report(done, total, f"{label}: strana {done}/{total}"),
                )
                exported += len(files)
            return exported

        def done(exported):
            messagebox.showinfo(APP_NAME, f"Exportovaných JPG súborov: {exported}", parent=self)
            self.set_status(f"Exportovaných JPG súborov: {exported}")

        self.run_in_background(work, done)

    def add_images_to_table(self):
        table_path = self.choose_table()
        if not table_path:
            return

        result = self.read_chosen_table(table_path)
        if result is None:
            return
        fieldnames, rows = result
        columns = self.ask_columns(fieldnames)
        if not columns:
            return

        mode = self.ask_choice("Typ pomenovania obrázkov", ["Cvičenie / Prednáška", "Dokument (vypracovanie / kniha)"])
        if mode is None:
            return
        if mode == 0:
            header = self.ask_lecture_header()
            if not header:
                return
            subject, prefix = header
            number = self.ask_number(prefix)
            if number is None:
                return
            base = naming.lecture_base(subject, prefix, number)
        else:
            pdfs = list_files(self.folder, "*.pdf")
            initial = pdfs[0].stem if len(pdfs) == 1 else None
            document_name = simpledialog.askstring(
                APP_NAME, "Názov dokumentu/PDF bez .pdf:", initialvalue=initial, parent=self
            )
            if not document_name:
                return
            base = naming.validate_base(document_name)

        changed, skipped = fields.add_images_to_rows(rows, columns, base)
        output = tables.output_path(table_path, "images")
        tables.write_anki_tsv(output, fieldnames, rows)

        message = f"Uložené: {output.name}\nUpravených buniek: {changed}"
        if skipped:
            preview = "\n".join(f"  riadok {row}, {column}: {value[:40]}" for row, column, value in skipped[:10])
            more = f"\n  … a ďalších {len(skipped) - 10}" if len(skipped) > 10 else ""
            message += f"\n\n⚠ Nečitateľné bunky (ostali bez zmeny): {len(skipped)}\n{preview}{more}"
        messagebox.showinfo(APP_NAME, message, parent=self)
        self.set_status(f"Uložené: {output.name}")

    def move_images_to_folder(self):
        source = self.choose_one(
            list_subfolders(self.folder), "Vyber zdrojový priečinok", "V tomto priečinku sa nenašli žiadne priečinky."
        )
        if not source:
            return

        files = media.image_files(source)
        if not files:
            messagebox.showinfo(APP_NAME, f"V {source.name} nie sú žiadne obrázky.", parent=self)
            return

        destination = filedialog.askdirectory(parent=self, title="Vyber cieľový priečinok (napr. collection.media)")
        if not destination:
            return

        action = self.ask_choice("Akcia", ["Kopírovať súbory", "Presunúť súbory"])
        if action is None:
            return

        plan = media.plan_transfer(files, Path(destination))
        if plan.changed:
            confirm = messagebox.askyesnocancel(
                APP_NAME,
                media.describe_plan(plan) + "\n\nPrepísať súbory s iným obsahom?\n"
                "Áno = prepísať, Nie = preskočiť ich, Zrušiť = nič nerobiť",
                parent=self,
            )
            if confirm is None:
                return
            overwrite = confirm
        else:
            overwrite = True

        done = media.execute_transfer(plan, move=(action == 1), overwrite_changed=overwrite)
        summary = f"Spracovaných: {done}, rovnakých preskočených: {len(plan.identical)}"
        if plan.changed and not overwrite:
            summary += f", s iným obsahom preskočených: {len(plan.changed)}"
        messagebox.showinfo(APP_NAME, summary, parent=self)
        self.set_status(summary)

    def extract_text_from_pdf(self):
        pdf_path = self.choose_pdf()
        if not pdf_path:
            return

        mode = self.ask_choice("Typ textu", ["Prednáška s oddeľovačmi strán", "Dokument - vyčistený text"])
        if mode is None:
            return

        output = pdf.extract_text(pdf_path, with_page_separators=(mode == 0))
        open_path(output)
        self.set_status(f"Uložené: {output.name}")

    def delete_pdf_pages(self):
        pdf_path = self.choose_pdf()
        if not pdf_path:
            return

        count = pdf.page_count(pdf_path)
        raw = simpledialog.askstring(
            APP_NAME, f"{pdf_path.name} má {count} strán.\nStrany na vymazanie, napr. 1,3,5-7:", parent=self
        )
        if not raw:
            return

        output = pdf.delete_pages(pdf_path, parse_pages(raw, count))
        messagebox.showinfo(APP_NAME, f"Uložené: {output.name}", parent=self)
        self.set_status(f"Uložené: {output.name}")

    def rename_pdf(self):
        pdf_path = self.choose_pdf()
        if not pdf_path:
            return

        new_name = simpledialog.askstring(APP_NAME, f"Nový názov pre {pdf_path.name} bez .pdf:", parent=self)
        if not new_name:
            return

        target = pdf.rename(pdf_path, naming.validate_base(new_name))
        messagebox.showinfo(APP_NAME, f"Premenované na: {target.name}", parent=self)
        self.set_status(f"Premenované na: {target.name}")

    def add_tags_to_table(self):
        table_files = self.choose_table(many=True)
        if not table_files:
            return

        tag = simpledialog.askstring(APP_NAME, "Tag, ktorý sa pridá tam, kde je Tags prázdne:", parent=self)
        if not tag or not tag.strip():
            return
        tag = tag.strip()

        messages = []
        for table_path in table_files:
            result = self.read_chosen_table(table_path)
            if result is None:
                continue
            fieldnames, rows = result
            if "Tags" not in fieldnames:
                messages.append(f"{table_path.name}: chýba stĺpec Tags")
                continue
            changed = fields.fill_empty_tags(rows, tag)
            output = tables.output_path(table_path, "tagged")
            tables.write_anki_tsv(output, fieldnames, rows)
            messages.append(f"{output.name}: upravených riadkov {changed}")

        messagebox.showinfo(APP_NAME, "\n".join(messages), parent=self)
        self.set_status("Tagy boli pridané.")

    def fix_back_column(self):
        table_path = self.choose_table()
        if not table_path:
            return

        result = self.read_chosen_table(table_path)
        if result is None:
            return
        fieldnames, rows = result
        if "Back" not in fieldnames:
            messagebox.showerror(
                APP_NAME, "Tento súbor nemá stĺpec Back.\n\nNájdené stĺpce:\n" + ", ".join(fieldnames), parent=self
            )
            return

        changed = fields.fix_back_rows(rows)
        output = tables.output_path(table_path, "fixed")
        tables.write_anki_tsv(output, fieldnames, rows)
        messagebox.showinfo(
            APP_NAME, f"Uložené: {output.name}\nUpravených riadkov: {changed}\n\nImport do Anki: File → Import → tento .tsv", parent=self
        )
        self.set_status(f"Uložené: {output.name}")


class ChooseFilesDialog(tk.Toplevel):
    def __init__(self, parent, title, paths, multiple):
        super().__init__(parent)
        self.withdraw()
        self.title(title)
        self.configure(bg=BG_DIALOG)
        self.transient(parent)
        self.grab_set()
        self.result = [] if multiple else None
        self.paths = paths
        self.multiple = multiple

        tk.Label(self, text=title, bg=BG_DIALOG, fg=FG, font=("Segoe UI", 14, "bold")).pack(pady=(16, 8))
        selectmode = tk.MULTIPLE if multiple else tk.BROWSE
        self.listbox = tk.Listbox(self, selectmode=selectmode, font=("Segoe UI", 11), bg=BG, fg=FG)
        self.listbox.pack(fill="both", expand=True, padx=18, pady=8)

        for path in paths:
            self.listbox.insert(tk.END, path.name)

        if multiple:
            tk.Label(self, text="Klik = označiť / odznačiť, Ctrl+A = všetky", bg=BG_DIALOG, fg=FG_MUTED,
                     font=("Segoe UI", 9)).pack()
            self.listbox.bind("<Control-a>", lambda _event: self.listbox.select_set(0, tk.END))

        buttons = tk.Frame(self, bg=BG_DIALOG)
        buttons.pack(fill="x", padx=18, pady=(6, 16))
        ttk.Button(buttons, text="Zrušiť", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="OK", command=self.ok).pack(side="right")

        self.listbox.bind("<Double-Button-1>", lambda _event: self.ok())
        self.listbox.bind("<Return>", lambda _event: self.ok())
        self.bind("<Escape>", lambda _event: self.destroy())
        center_window(self, parent, 520, 400)
        self.deiconify()
        self.listbox.focus_set()
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
        self.configure(bg=BG_DIALOG)
        self.transient(parent)
        self.grab_set()
        self.result = None

        tk.Label(self, text=title, bg=BG_DIALOG, fg=FG, font=("Segoe UI", 13, "bold")).pack(padx=18, pady=(16, 8))
        for index, choice in enumerate(choices):
            ttk.Button(self, text=f"{index + 1}. {choice}", command=lambda i=index: self.choose(i)).pack(
                fill="x", padx=18, pady=5
            )
            self.bind(str(index + 1), lambda _event, i=index: self.choose(i))
        ttk.Button(self, text="Zrušiť", command=self.destroy).pack(fill="x", padx=18, pady=(12, 16))
        self.bind("<Escape>", lambda _event: self.destroy())

        center_window(self, parent)
        self.deiconify()
        self.focus_set()
        self.wait_window()

    def choose(self, index):
        self.result = index
        self.destroy()


class CheckboxDialog(tk.Toplevel):
    def __init__(self, parent, title, options):
        super().__init__(parent)
        self.withdraw()
        self.title(title)
        self.configure(bg=BG_DIALOG)
        self.transient(parent)
        self.grab_set()
        self.result = []
        self.vars = []

        tk.Label(self, text=title, bg=BG_DIALOG, fg=FG, font=("Segoe UI", 13, "bold")).pack(padx=18, pady=(16, 8))
        box = tk.Frame(self, bg=BG_DIALOG)
        box.pack(fill="x", padx=18)

        for option in options:
            var = tk.BooleanVar(value=True)
            self.vars.append((option, var))
            tk.Checkbutton(
                box,
                text=option,
                variable=var,
                bg=BG_DIALOG,
                fg=FG,
                selectcolor=BG,
                activebackground=BG_DIALOG,
                activeforeground="#ffffff",
                font=("Segoe UI", 11),
            ).pack(anchor="w", pady=3)

        buttons = tk.Frame(self, bg=BG_DIALOG)
        buttons.pack(fill="x", padx=18, pady=(12, 16))
        ttk.Button(buttons, text="Zrušiť", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="OK", command=self.ok).pack(side="right")
        self.bind("<Return>", lambda _event: self.ok())
        self.bind("<Escape>", lambda _event: self.destroy())

        center_window(self, parent)
        self.deiconify()
        self.focus_set()
        self.wait_window()

    def ok(self):
        self.result = [option for option, var in self.vars if var.get()]
        self.destroy()


if __name__ == "__main__":
    AnkiGui().mainloop()
