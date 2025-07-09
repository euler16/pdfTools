#!/usr/bin/env python3
"""
merge_to_pdf.py

Merge every JPG/JPEG/PNG image and/or PDF in a directory into a single PDF.
Files are processed in **lexicographic order** of their names.

Usage
-----
$ python merge_to_pdf.py /path/to/input_dir merged.pdf

• If `merged.pdf` already exists it will be overwritten.
• Only the top-level of `input_dir` is scanned (no recursion).

Dependencies
------------
pip install Pillow PyPDF2
"""

import argparse
import io
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

from PIL import Image
from PyPDF2 import PdfMerger, PdfReader


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def images_to_pdf_bytes(image_path: Path) -> bytes:
    """Convert a single image file to PDF bytes in memory."""
    with Image.open(image_path) as img:
        # Pillow requires RGB for PDF export; discard alpha if present
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="PDF", resolution=300.0)
        return buffer.getvalue()


def add_file_to_merger(f: Path, merger: PdfMerger) -> None:
    """Append an image or PDF file to the PdfMerger."""
    suffix = f.suffix.lower()
    if suffix == ".pdf":
        merger.append(PdfReader(str(f), strict=False))
    elif suffix in IMAGE_EXTS:
        pdf_bytes = images_to_pdf_bytes(f)
        # Use a NamedTemporaryFile so PdfMerger can read from a real file path
        with NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
            tmp.write(pdf_bytes)
            tmp.flush()
            merger.append(PdfReader(tmp.name, strict=False))
    else:
        print(f"Skipped unsupported file: {f}", file=sys.stderr)


def merge_directory(input_dir: Path, output_pdf: Path) -> None:
    """Walk directory, merge supported files, and write output_pdf."""
    files = sorted(
        [p for p in input_dir.iterdir() if p.is_file()], key=lambda p: p.name.lower()
    )

    if not files:
        raise SystemExit(f"No supported files found in {input_dir}")

    merger = PdfMerger()

    for f in files:
        add_file_to_merger(f, merger)

    merger.write(str(output_pdf))
    merger.close()
    print(f"✔ Merged {len(files)} items into {output_pdf}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge JPG/PNG/TIFF and PDF files in a directory into one PDF."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing files to merge",
    )
    parser.add_argument(
        "output_pdf",
        type=Path,
        nargs="?",
        default=Path("merged.pdf"),
        help="Path for the merged PDF (default: ./merged.pdf)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input_dir.is_dir():
        raise SystemExit(f"{args.input_dir} is not a directory or does not exist.")

    try:
        merge_directory(args.input_dir, args.output_pdf)
    except Exception as exc:
        raise SystemExit(f"Failed to merge: {exc}") from exc


if __name__ == "__main__":
    main()
