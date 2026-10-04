"""Parsovanie čísel strán – z dialógu aj z buniek tabuľky."""

import re

from . import MAX_PAGES_PER_CELL

_RANGE_SPACES = re.compile(r"\s*[-–]\s*")
_SEPARATORS = re.compile(r"[,;\s]+")
_TOKEN = re.compile(r"^(\d+)(?:\.0+)?(?:-(\d+)(?:\.0+)?)?$")


def parse_pages(raw, page_count):
    """Vstup '1,3,5-7' -> množina 0-based indexov. Pre mazanie strán z PDF."""
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

    invalid = sorted(page for page in pages if page < 1 or page > page_count)
    if invalid:
        raise ValueError(f"Neplatné číslo strany: {invalid}")
    return {page - 1 for page in pages}


def parse_cell_pages(value):
    """Bunka s číslami strán -> zoznam strán (poradie zachované, bez duplikátov).

    Podporuje: '12', '12.0', '1,2,10', '1;2', '1 2', '5-7', '1, 5–7'.
    Ak bunka obsahuje čokoľvek iné (text, HTML, už hotový <img>),
    vráti None – taká bunka sa nemení.
    """
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None

    text = _RANGE_SPACES.sub("-", text)
    pages = []
    for token in _SEPARATORS.split(text):
        if not token:
            continue
        match = _TOKEN.match(token)
        if not match:
            return None
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else start
        if start > end:
            start, end = end, start
        if start < 1:
            return None
        if end - start + 1 > MAX_PAGES_PER_CELL:
            return None
        for page in range(start, end + 1):
            if page not in pages:
                pages.append(page)

    if not pages or len(pages) > MAX_PAGES_PER_CELL:
        return None
    return pages
