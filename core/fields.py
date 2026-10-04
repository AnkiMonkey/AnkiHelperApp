"""Úpravy obsahu polí pred importom do Anki."""

import re

from .naming import images_html
from .pages import parse_cell_pages

# Svaly: O = odstup, U = úpon, I = inervácia, F = funkcia
_MUSCLE_LINE_BREAK = re.compile(r"\s+([UFIO]:)")
_MUSCLE_BOLD = re.compile(r"(?<!<b>)([UFIO]:)(?!</b>)")


def fix_back_field(text):
    """Každá časť O:/U:/I:/F: na nový riadok a tučne. Dá sa spustiť opakovane."""
    if text is None:
        return ""
    text = str(text).strip()
    text = _MUSCLE_LINE_BREAK.sub(r"<br>\1", text)
    text = _MUSCLE_BOLD.sub(r"<b>\1</b>", text)
    return text


def add_images_to_rows(rows, columns, base):
    """Čísla strán v bunkách -> <img> tagy.

    Vráti (changed, skipped):
      changed – počet upravených buniek
      skipped – zoznam (číslo_riadku, stĺpec, hodnota) buniek, ktoré neboli
                prázdne, ale nedali sa prečítať ako čísla strán
    """
    changed, skipped = 0, []
    for row_number, row in enumerate(rows, start=2):  # riadok 1 = hlavička
        for column in columns:
            value = row.get(column)
            if value is None or not str(value).strip():
                continue
            pages = parse_cell_pages(value)
            if pages is None:
                if "<img" not in str(value):
                    skipped.append((row_number, column, str(value)))
                continue
            row[column] = images_html(base, pages)
            changed += 1
    return changed, skipped


def fill_empty_tags(rows, tag):
    changed = 0
    for row in rows:
        if not str(row.get("Tags", "") or "").strip():
            row["Tags"] = tag
            changed += 1
    return changed


def fix_back_rows(rows):
    changed = 0
    for row in rows:
        old_value = row.get("Back", "")
        new_value = fix_back_field(old_value)
        if old_value != new_value:
            changed += 1
        row["Back"] = new_value
    return changed
