import pytest

pymupdf = pytest.importorskip("pymupdf")

from core import pdf  # noqa: E402


@pytest.fixture
def sample_pdf(tmp_path):
    path = tmp_path / "V PharmII02.pdf"
    document = pymupdf.open()
    for index in range(3):
        page = document.new_page()
        page.insert_text((72, 72), f"Strana {index + 1}")
    document.save(path)
    document.close()
    return path


def test_export_jpg(tmp_path, sample_pdf):
    calls = []
    files = pdf.export_jpg(sample_pdf, tmp_path / "out", "PharmII_P_02", dpi=72,
                           progress=lambda d, t: calls.append((d, t)))
    assert [f.name for f in files] == [f"PharmII_P_02_S_0{i}.jpg" for i in (1, 2, 3)]
    assert all(f.stat().st_size > 0 for f in files)
    assert calls[-1] == (3, 3)


def test_delete_extract_rename(sample_pdf):
    output = pdf.delete_pages(sample_pdf, {0})
    assert pdf.page_count(output) == 2
    assert pdf.page_count(sample_pdf) == 3  # originál nedotknutý

    with pytest.raises(ValueError):
        pdf.delete_pages(sample_pdf, {0, 1, 2})

    text = pdf.extract_text(sample_pdf).read_text(encoding="utf-8")
    assert "Toto je strana 3" in text and "Strana 2" in text

    renamed = pdf.rename(sample_pdf, "PharmII_V02.pdf")
    assert renamed.name == "PharmII_V02.pdf"
    with pytest.raises(FileExistsError):
        pdf.rename(output, "PharmII_V02")
