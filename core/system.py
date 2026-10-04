import os
import subprocess
import sys
from pathlib import Path


def app_folder():
    """Priečinok, kde leží skript alebo .exe (PyInstaller)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def open_path(path):
    """Otvorí súbor/priečinok v predvolenej aplikácii (Windows, macOS, Linux)."""
    path = str(path)
    if os.name == "nt":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def list_files(folder, pattern):
    return sorted(Path(folder).glob(pattern), key=lambda path: path.name.lower())


def list_tables(folder):
    """CSV, TSV a XLSX súbory v priečinku (bez dočasných ~$ súborov Excelu)."""
    files = []
    for pattern in ("*.csv", "*.tsv", "*.xlsx", "*.xlsm"):
        files += [path for path in list_files(folder, pattern) if not path.name.startswith("~$")]
    return sorted(files, key=lambda path: path.name.lower())


def list_subfolders(folder):
    return [path for path in sorted(Path(folder).iterdir(), key=lambda item: item.name.lower()) if path.is_dir()]
