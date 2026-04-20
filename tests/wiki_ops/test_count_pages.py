"""Parity tests for ``motion.wiki_ops.count_pages``.

The TS original prints ``"  {pages:>4} pp  {filename}"`` per sorted PDF
and a footer ``"\\n  {total} pages total across {n} PDFs"``. Because
the Python port uses pypdfium2 and the TS original used pdf-lib, the
actual page counts returned from the two libraries must agree on the
same PDF. We exercise that with a tiny pure-Python-generated PDF so
the test never depends on the raw/ corpus.
"""

from __future__ import annotations

from pathlib import Path

import pypdfium2
import pytest

from motion.wiki_ops.count_pages import count_pages_in_dir, format_report


def _write_minimal_pdf(path: Path, page_count: int) -> None:
    """Write a PDF with ``page_count`` empty A4 pages using pypdfium2.

    Rather than hand-roll PDF bytes (PDFium is strict about xref
    layout), we use the documented ``PdfDocument.new()``/``new_page``
    API — verified via Context7 on 2026-04-13
    (``/pypdfium2-team/pypdfium2`` README).
    """
    pdf = pypdfium2.PdfDocument.new()
    try:
        width, height = 595, 842  # A4
        for _ in range(page_count):
            pdf.new_page(width, height)
        pdf.save(str(path))
    finally:
        close = getattr(pdf, "close", None)
        if callable(close):
            close()


@pytest.fixture()
def pdf_dir(tmp_path: Path) -> Path:
    d = tmp_path / "raw"
    d.mkdir()
    # Intentionally out of lexicographic order to verify sort().
    _write_minimal_pdf(d / "beta.pdf", 3)
    _write_minimal_pdf(d / "alpha.pdf", 7)
    _write_minimal_pdf(d / "gamma.pdf", 12)
    (d / "not-a-pdf.txt").write_text("ignore me")
    return d


def test_count_pages_sorted_totals(pdf_dir: Path) -> None:
    results, total = count_pages_in_dir(pdf_dir)
    assert [name for name, _ in results] == ["alpha.pdf", "beta.pdf", "gamma.pdf"]
    assert [pages for _, pages in results] == [7, 3, 12]
    assert total == 22


def test_format_report_matches_ts_shape(pdf_dir: Path) -> None:
    results, total = count_pages_in_dir(pdf_dir)
    report = format_report(results, total)
    expected = (
        "     7 pp  alpha.pdf\n"
        "     3 pp  beta.pdf\n"
        "    12 pp  gamma.pdf\n"
        "\n"
        "  22 pages total across 3 PDFs\n"
    )
    assert report == expected


def test_format_report_empty_directory() -> None:
    report = format_report([], 0)
    # ``\n  0 pages total across 0 PDFs\n`` matches a single ``console.log`` call.
    assert report == "\n  0 pages total across 0 PDFs\n"


def test_count_pages_ignores_non_pdf_entries(pdf_dir: Path) -> None:
    results, _ = count_pages_in_dir(pdf_dir)
    names = [name for name, _ in results]
    assert "not-a-pdf.txt" not in names


def test_count_pages_missing_dir_raises(tmp_path: Path) -> None:
    missing = tmp_path / "nope"
    with pytest.raises(FileNotFoundError):
        count_pages_in_dir(missing)
