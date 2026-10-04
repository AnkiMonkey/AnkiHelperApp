"""Jednotné pomenovanie obrázkov – export aj HTML tagy musia sedieť 1:1."""

import re

LECTURE_PREFIXES = {"Cvičenie": "C", "Prednáška": "P"}


def lecture_base(subject, prefix, number):
    """'O-CHEM1', 'P', 1 -> 'O-CHEM1_P_01'"""
    return f"{subject.strip()}_{prefix}_{int(number):02d}"


def page_filename(base, page):
    """Vždy aspoň 2 cifry: S_01 … S_99, S_100 … – export aj tagy používajú túto funkciu."""
    return f"{base}_S_{int(page):02d}.jpg"


def image_tag(filename):
    """Čistý tag bez width – veľkosť rieši CSS notetypu."""
    return f'<img src="{filename}">'


def images_html(base, pages):
    return "<br>".join(image_tag(page_filename(base, page)) for page in pages)


_INVALID_CHARS = re.compile(r'[<>:"/\\|?*]')


def validate_base(base):
    """Názov musí byť platný ako názov súboru na Windows."""
    base = base.strip()
    if not base:
        raise ValueError("Názov nesmie byť prázdny.")
    if _INVALID_CHARS.search(base):
        raise ValueError(f"Názov obsahuje nepovolené znaky: {base}")
    return base


def find_duplicate_bases(bases):
    """Vráti názvy, ktoré sa v jednom behu opakujú (=> kolízia obrázkov)."""
    seen, duplicates = set(), []
    for base in bases:
        if base in seen and base not in duplicates:
            duplicates.append(base)
        seen.add(base)
    return duplicates
