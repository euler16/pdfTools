#!/usr/bin/env python3
"""
split_pdf.py  –  Split or extract pages from a PDF.

Examples
--------
# 1. One‑file‑per‑page (default)
python split_pdf.py report.pdf out_dir/

# 2. Extract pages 1‑3, page 5, and pages 7‑9
python split_pdf.py report.pdf out_dir/ --ranges 1-3,5,7-9

# 3. Overwrite output files if they exist
python split_pdf.py report.pdf out_dir/ --overwrite
"""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import List, Tuple

from pypdf import PdfReader, PdfWriter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_ranges(ranges_str: str) -> List[Tuple[int, int]]:
    """
    Convert '1-3,5,7-9' → [(1,3), (5,5), (7,9)]  (1‑based, inclusive).
    """
    result: List[Tuple[int, int]] = []
    for part in ranges_str.split(","):
        part = part.strip()
        if "-" in part:
            a, b = (int(x) for x in part.split("-", 1))
            if a > b:
                raise ValueError(f"Range start > end in '{part}'")
            result.append((a, b))
        else:
            p = int(part)
            result.append((p, p))
    return result


def add_pages(writer: PdfWriter, reader: PdfReader, start: int, end: int) -> None:
    """Add pages [start‑1, end‑1] (1‑based inclusive) to *writer*."""
    for i in range(start - 1, end):
        if i >= len(reader.pages) or i < 0:
            raise IndexError(f"Page {i + 1} is out of bounds")
        writer.add_page(reader.pages[i])


def write_pdf(writer: PdfWriter, path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists (use --overwrite to replace)")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        writer.write(fh)


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def split_pdf(
    src: Path,
    dest_dir: Path,
    ranges: List[Tuple[int, int]] | None,
    overwrite: bool = False,
) -> None:
    reader = PdfReader(str(src))
    dest_dir.mkdir(parents=True, exist_ok=True)

    if ranges is None:
        # One file per page
        for page_no, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)
            out_path = dest_dir / f"{src.stem}_p{page_no}.pdf"
            write_pdf(writer, out_path, overwrite)
    else:
        # One file per range
        for idx, (start, end) in enumerate(ranges, start=1):
            writer = PdfWriter()
            add_pages(writer, reader, start, end)
            label = f"{start}" if start == end else f"{start}-{end}"
            out_path = dest_dir / f"{src.stem}_{label}.pdf"
            write_pdf(writer, out_path, overwrite)


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Split a PDF into pages or extract page ranges."
    )
    parser.add_argument("pdf", type=Path, help="Input PDF file")
    parser.add_argument("out_dir", type=Path, help="Output directory")
    parser.add_argument(
        "--ranges",
        help="Comma‑separated list of pages or ranges (e.g. 1-3,5,7-9). "
        "If omitted, every page is split into its own PDF.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing files in the output directory",
    )
    args = parser.parse_args()

    ranges = parse_ranges(args.ranges) if args.ranges else None
    split_pdf(args.pdf, args.out_dir, ranges, overwrite=args.overwrite)
    print("✅ Done.")


if __name__ == "__main__":
    cli()
