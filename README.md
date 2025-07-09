# PDF Tools Suite

```
██████╗ ██████╗ ███████╗    ████████╗ ██████╗  ██████╗ ██╗     ███████╗
██╔══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
██████╔╝██║  ██║█████╗         ██║   ██║   ██║██║   ██║██║     ███████╗
██╔═══╝ ██║  ██║██╔══╝         ██║   ██║   ██║██║   ██║██║     ╚════██║
██║     ██████╔╝██║            ██║   ╚██████╔╝╚██████╔╝███████╗███████║
╚═╝     ╚═════╝ ╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                                        
   ███████╗██╗   ██╗██╗████████╗███████╗                               
   ██╔════╝██║   ██║██║╚══██╔══╝██╔════╝                               
   ███████╗██║   ██║██║   ██║   █████╗                                 
   ╚════██║██║   ██║██║   ██║   ██╔══╝                                 
   ███████║╚██████╔╝██║   ██║   ███████╗                               
   ╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚══════╝                               
```

A comprehensive collection of Python tools for PDF manipulation, including compression, splitting, and merging operations.

## 📋 Overview

This suite provides three powerful PDF utilities:

- **PDF Compressor**: Reduce PDF file sizes using Ghostscript with various quality presets
- **PDF Splitter**: Split PDFs into individual pages or extract specific page ranges
- **PDF Merger**: Combine multiple PDFs and images into a single PDF file

## 🛠️ Tools Included

### 1. PDF Compressor (`pdf_compressor/`)
Compress PDF files to reduce their size while maintaining quality control.

**Features:**
- Multiple compression levels (screen, ebook, printer, prepress, default)
- File size comparison with reduction percentage
- Batch processing support
- Human-readable file size display

### 2. PDF Splitter (`pdf_splitter/`)
Split PDF files into separate pages or extract specific page ranges.

**Features:**
- One-file-per-page splitting
- Custom page range extraction
- Flexible range syntax (e.g., 1-3,5,7-9)
- Overwrite protection with optional force mode

### 3. PDF Merger (`pdf_merger/`)
Merge multiple PDF files and images into a single PDF document.

**Features:**
- Supports PDF, JPG, JPEG, PNG, TIF, and TIFF files
- Lexicographic file ordering
- High-resolution image conversion (300 DPI)
- Memory-efficient processing

## 📦 Installation

### Prerequisites

1. **Python 3.7+** is required
2. **Ghostscript** (for PDF compression):
   ```bash
   # macOS
   brew install ghostscript
   
   # Ubuntu/Debian
   sudo apt-get install ghostscript
   
   # Windows
   # Download from https://www.ghostscript.com/download/gsdnld.html
   ```

### Dependencies

Install the required Python packages:

```bash
pip install pypdf PyPDF2 Pillow
```

Or create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pypdf PyPDF2 Pillow
```

## 🚀 Usage

### PDF Compressor

```bash
cd pdf_compressor/

# Basic compression (default: ebook quality)
python compress_pdf2.py input.pdf

# Specify compression level
python compress_pdf2.py input.pdf -c screen

# Custom output path
python compress_pdf2.py input.pdf -o compressed_output.pdf

# Force overwrite existing file
python compress_pdf2.py input.pdf -f

# View all options
python compress_pdf2.py -h
```

**Compression Levels:**
- `screen`: Screen-view-only quality, 72 dpi images
- `ebook`: Low quality, 150 dpi images (default)
- `printer`: High quality, 300 dpi images
- `prepress`: High quality preserving color, 300 dpi images
- `default`: Almost identical to screen

### PDF Splitter

```bash
cd pdf_splitter/

# Split into individual pages
python split_pdf.py document.pdf output_directory/

# Extract specific page ranges
python split_pdf.py document.pdf output_directory/ --ranges 1-3,5,7-9

# Overwrite existing files
python split_pdf.py document.pdf output_directory/ --overwrite

# View all options
python split_pdf.py -h
```

**Range Syntax:**
- `1-3`: Pages 1 through 3
- `5`: Single page 5
- `7-9`: Pages 7 through 9
- `1-3,5,7-9`: Multiple ranges combined

### PDF Merger

```bash
cd pdf_merger/

# Merge all files in a directory
python merge_to_pdf.py input_directory/ merged_output.pdf

# Use default output name (merged.pdf)
python merge_to_pdf.py input_directory/

# View all options
python merge_to_pdf.py -h
```

**Supported File Types:**
- PDF files (`.pdf`)
- Image files (`.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`)

## 📁 Project Structure

```
pdf-tools-suite/
├── README.md
├── pdf_compressor/
│   ├── compress_pdf2.py
│   └── [sample PDFs]
├── pdf_merger/
│   ├── merge_to_pdf.py
│   ├── input_dir/
│   └── [output PDFs]
└── pdf_splitter/
    ├── split_pdf.py
    ├── splits/
    └── [sample PDFs]
```

## 💡 Examples

### Example 1: Compress a large PDF
```bash
cd pdf_compressor/
python compress_pdf2.py large_document.pdf -c ebook
```

### Example 2: Extract specific pages
```bash
cd pdf_splitter/
python split_pdf.py report.pdf extracted_pages/ --ranges 1-5,10,15-20
```

### Example 3: Merge images and PDFs
```bash
cd pdf_merger/
# Place your PDFs and images in input_dir/
python merge_to_pdf.py input_dir/ final_document.pdf
```

## 🔧 Troubleshooting

### Common Issues

1. **Ghostscript not found**: Make sure Ghostscript is installed and in your PATH
2. **Permission errors**: Check file permissions and write access to output directories
3. **Memory issues**: For large files, ensure sufficient system memory
4. **Corrupted PDFs**: Some PDFs may need repair before processing

### Error Messages

- `FileNotFoundError`: Input file doesn't exist or path is incorrect
- `FileExistsError`: Output file already exists (use `-f` or `--overwrite`)
- `subprocess.CalledProcessError`: Ghostscript execution failed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue in the project repository.

---

**Happy PDF Processing!** 🎉
