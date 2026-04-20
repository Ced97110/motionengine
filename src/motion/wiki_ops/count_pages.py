"""Count pages across every PDF in the raw-source directory.

Port of ``frontend/scripts/count-pages.ts``. Behavior is byte-equal: for
each ``*.pdf`` in ``backend/knowledge-base/raw/`` (sorted
lexicographically), print ``"  {pages:>4} pp  {filename}"`` on its own
line. After the last PDF print a blank line followed by
``"  {total} pages total across {n} PDFs"``.

pypdfium2 API used (verified via Context7 ``/pypdfium2-team/pypdfium2``
README, 2026-04-13):

- ``pypdfium2.PdfDocument(path)`` opens a document from a filesystem
  path.
- ``len(doc)`` returns the page count.

The TS original passed ``ignoreEncryption: true`` to ``pdf-lib`` as a
defensive measure against optionally-encrypted PDFs. PDFium requires a
password only for *encrypted* documents; none of the nine shipped raw
PDFs are encrypted, so no password handling is wired in here.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pypdfium2

from .paths import raw_pdf_dir


def count_pages_in_dir(directory: Path) -> tuple[list[tuple[str, int]], int]:
    """Return ``([(filename, page_count), ...], total_pages)``.

    Files are returned in lexicographic order to match
    ``fs.readdir(...).sort()`` in the TS original.
    """
    if not directory.is_dir():
        raise FileNotFoundError(f"Raw PDF directory not found: {directory}")
    pdfs = sorted(p.name for p in directory.iterdir() if p.is_file() and p.name.endswith(".pdf"))
    results: list[tuple[str, int]] = []
    total = 0
    for name in pdfs:
        # ``PdfDocument`` exposes a ``close()`` method that releases the
        # underlying PDFium handle. Newer versions additionally support
        # the context-manager protocol (see
        # ``/pypdfium2-team/pypdfium2`` changelog via Context7,
        # 2026-04-13). We call ``close()`` explicitly so the same code
        # path works across both the older and newer releases pinned by
        # ``pypdfium2>=5.7``.
        doc = pypdfium2.PdfDocument(str(directory / name))
        try:
            pages = len(doc)
        finally:
            close = getattr(doc, "close", None)
            if callable(close):
                close()
        results.append((name, pages))
        total += pages
    return results, total


def format_report(results: list[tuple[str, int]], total: int) -> str:
    """Format the stdout output to match the TS ``console.log`` sequence.

    Each ``console.log`` call in Node appends a ``\\n``, so the expected
    byte sequence is:

    ``"  {pages:>4} pp  {name}\\n"`` per file, then a blank
    ``console.log()`` which is ``"\\n"``, then
    ``"  {total} pages total across {n} PDFs\\n"``.

    Because the TS writes ``"\\n  {total}..."`` via a single
    ``console.log("\\n...")`` call, the bytes are
    ``"\\n  {total} pages total across {n} PDFs\\n"``. The trailing
    newline comes from ``console.log`` itself.
    """
    lines: list[str] = []
    for name, pages in results:
        lines.append(f"  {pages:>4} pp  {name}\n")
    # Single console.log(`\n  ${total} pages total across ${files.length} PDFs`)
    # emits "\n  ...\n".
    lines.append(f"\n  {total} pages total across {len(results)} PDFs\n")
    return "".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point. Writes to ``stdout`` and returns an exit code."""
    parser = argparse.ArgumentParser(
        prog="wiki-count-pages",
        description="Count pages across every PDF in the raw-source directory.",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=None,
        help="Override the raw PDF directory (default: backend/knowledge-base/raw).",
    )
    args = parser.parse_args(argv)
    directory = raw_pdf_dir(args.raw_dir)
    try:
        results, total = count_pages_in_dir(directory)
    except FileNotFoundError as exc:
        sys.stderr.write(f"count-pages failed: {exc}\n")
        return 1
    sys.stdout.write(format_report(results, total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
