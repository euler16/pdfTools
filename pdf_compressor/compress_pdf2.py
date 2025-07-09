#!/usr/bin/env python3
"""
PDF Compressor: A tool to reduce the size of PDF files through optimization.

This script uses Ghostscript to compress PDF files with various quality presets.
Ghostscript must be installed on your system for this script to work.

Installation of Ghostscript:
- Windows: Download from https://www.ghostscript.com/download/gsdnld.html
- Linux: sudo apt-get install ghostscript
- macOS: brew install ghostscript
"""

import os
import subprocess
import argparse
import time
from pathlib import Path

# Available compression presets
COMPRESSION_LEVELS = {
    "screen": "Screen-view-only quality, 72 dpi images",
    "ebook": "Low quality, 150 dpi images",
    "printer": "High quality, 300 dpi images",
    "prepress": "High quality preserving color, 300 dpi imgs",
    "default": "Almost identical to screen",
}


def get_file_size(file_path):
    """Get file size in bytes and format it as human-readable."""
    size_bytes = os.path.getsize(file_path)
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} GB"


def compress_pdf(input_path, output_path=None, compression_level="ebook", force=False):
    """
    Compress a PDF file using Ghostscript with the specified compression level.

    Args:
        input_path (str): Path to the input PDF file
        output_path (str, optional): Path for the output PDF file
        compression_level (str): Level of compression (screen, ebook, printer, prepress, default)
        force (bool): Whether to overwrite output file if it exists

    Returns:
        str: Path to the compressed file
    """
    # Validate input file
    input_path = os.path.abspath(input_path)
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Set output path if not provided
    if output_path is None:
        dir_path, filename = os.path.split(input_path)
        base_name, ext = os.path.splitext(filename)
        output_path = os.path.join(dir_path, f"{base_name}_compressed{ext}")

    # Validate output path
    output_path = os.path.abspath(output_path)
    if os.path.exists(output_path) and not force:
        raise FileExistsError(f"Output file already exists: {output_path}")

    # Check if the compression level is valid
    if compression_level not in COMPRESSION_LEVELS.keys():
        raise ValueError(
            f"Invalid compression level. Choose from: {', '.join(COMPRESSION_LEVELS.keys())}"
        )

    # Get the input file size before compression
    input_size = get_file_size(input_path)

    print(f"Compressing PDF: {input_path}")
    print(
        f"Compression level: {compression_level} ({COMPRESSION_LEVELS[compression_level]})"
    )

    # Prepare the Ghostscript command
    gs_command = [
        "gs",
        "-sDEVICE=pdfwrite",
        f"-dPDFSETTINGS=/{compression_level}",
        "-dCompatibilityLevel=1.4",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_path}",
        input_path,
    ]

    # Execute the command
    try:
        start_time = time.time()
        subprocess.run(gs_command, check=True)
        end_time = time.time()

        # Compare file sizes
        if os.path.exists(output_path):
            output_size = get_file_size(output_path)
            input_bytes = os.path.getsize(input_path)
            output_bytes = os.path.getsize(output_path)

            if output_bytes > 0 and input_bytes > 0:
                reduction = (1 - (output_bytes / input_bytes)) * 100
                print(f"\nCompression successful!")
                print(f"Original size: {input_size}")
                print(f"Compressed size: {output_size}")
                print(f"Reduction: {reduction:.1f}%")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                print(f"Output saved to: {output_path}")
                return output_path
            else:
                print("Warning: Could not calculate size reduction")
                return output_path
        else:
            raise FileNotFoundError(f"Output file was not created: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"Error running Ghostscript: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        raise
    except Exception as e:
        print(f"Compression failed: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        raise


def main():
    """Parse command line arguments and run the PDF compression."""
    parser = argparse.ArgumentParser(
        description="Compress PDF files using Ghostscript.",
        epilog=f"Available compression levels:\n"
        + "\n".join([f"  {k}: {v}" for k, v in COMPRESSION_LEVELS.items()]),
    )
    parser.add_argument("input", help="Path to the input PDF file")
    parser.add_argument(
        "-o",
        "--output",
        help="Path for the output PDF file (default: filename_compressed.pdf)",
    )
    parser.add_argument(
        "-c",
        "--compression",
        choices=COMPRESSION_LEVELS.keys(),
        default="ebook",
        help="Compression level (default: ebook)",
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite output file if it exists"
    )

    args = parser.parse_args()

    try:
        compress_pdf(args.input, args.output, args.compression, args.force)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
