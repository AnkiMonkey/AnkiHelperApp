"""PDF operácie (PyMuPDF)."""

import re

from . import JPEG_QUALITY, JPEG_SUBSAMPLING
from .naming import page_filename


def _pymupdf():
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError as error:
            raise RuntimeError("Chýba knižnica PyMuPDF: pip install pymupdf") from error
    return pymupdf


def page_count(pdf_path):
    pymupdf = _pymupdf()
    with pymupdf.open(pdf_path) as document:
        return document.page_count


def export_jpg(pdf_path, output_folder, base, dpi, quality=JPEG_QUALITY, progress=None):
    """Exportuje všetky strany. progress(done, total) sa volá po každej strane."""
    pymupdf = _pymupdf()
    from PIL import Image

    output_folder.mkdir(exist_ok=True)
    written = []
    with pymupdf.open(pdf_path) as document:
        total = document.page_count
        for page_index in range(total):
            page = document.load_page(page_index)
            pix = page.get_pixmap(dpi=dpi, alpha=False)
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            target = output_folder / page_filename(base, page_index + 1)
            image.save(target, "JPEG", quality=quality, subsampling=JPEG_SUBSAMPLING, optimize=True)
            written.append(target)
            if progress:
                progress(page_index + 1, total)
    return written


_OMIT_PATTERN = re.compile(r"Zoznam ot.+ / \d+\. strana")


def extract_text(pdf_path, with_page_separators=True):
    """Vráti cestu k .txt súboru."""
    pymupdf = _pymupdf()
    output_path = pdf_path.with_suffix(".txt")
    with pymupdf.open(pdf_path) as document, output_path.open("w", encoding="utf-8") as text_file:
        if with_page_separators:
            text_file.write(f"Toto je prepis z {pdf_path.stem}\n\n")
            for index, page in enumerate(document, start=1):
                text_file.write("\n" + "-" * 19 + f"\nToto je strana {index}\n\n")
                text_file.write(page.get_text() or "")
        else:
            for page in document:
                page_text = page.get_text() or "[Žiadny extrahovateľný text]\n"
                lines = [line for line in page_text.splitlines() if not _OMIT_PATTERN.match(line)]
                text_file.write("\n".join(lines) + "\n")
    return output_path


def delete_pages(pdf_path, pages_to_delete):
    """pages_to_delete = množina 0-based indexov. Originál ostane nedotknutý."""
    pymupdf = _pymupdf()
    with pymupdf.open(pdf_path) as document:
        keep = [index for index in range(document.page_count) if index not in pages_to_delete]
        if not keep:
            raise ValueError("PDF nemôže ostať bez strán.")
        output_path = pdf_path.with_name(f"{pdf_path.stem}_modified.pdf")
        document.select(keep)
        document.save(output_path)
    return output_path


def rename(pdf_path, new_stem):
    new_stem = new_stem.strip()
    if new_stem.lower().endswith(".pdf"):
        new_stem = new_stem[:-4]
    target = pdf_path.with_name(f"{new_stem}.pdf")
    if target.exists():
        raise FileExistsError(f"{target.name} už existuje.")
    pdf_path.rename(target)
    return target
