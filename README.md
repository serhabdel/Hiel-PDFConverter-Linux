# Hiel PDF Converter

A modern desktop application for converting PDF files to various formats using Python and Flet.

## Features

- **Multiple Format Support**: Convert PDFs to Text, Word, HTML, Markdown, and Images
- **Advanced Image Quality Control**: Customizable DPI, format (JPEG/PNG), and compression settings
- **Clean Architecture**: Built with Domain-Driven Design principles
- **Modern Scrollable UI**: Beautiful desktop interface built with Flet with responsive scrolling
- **Real-time Size Estimation**: Live preview of output file sizes based on settings
- **Smart Compression**: Up to 85% size reduction with optimized JPEG compression
- **Cross-Platform**: Works on Linux, Windows, and macOS
- **Robust Error Handling**: Comprehensive error handling and user feedback

## Supported Conversion Formats

- **Text** (.txt) - Plain text extraction
- **Word** (.docx) - Microsoft Word document
- **HTML** (.html) - Web page format
- **Markdown** (.md) - Markdown format
- **Images** (.png) - High-quality image conversion

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd "Hiel Converter Linux"
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Pandoc (required for Word, HTML, and Markdown conversion):**
   - **Ubuntu/Debian:** `sudo apt-get install pandoc`
   - **macOS:** `brew install pandoc`
   - **Windows:** Download from https://pandoc.org/installing.html

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Convert a PDF:**
   - Click "Browse PDF" to select your PDF file
   - Choose the desired output format from the dropdown
   - Click "Select Output Location" to choose where to save the converted file
   - Click "Convert PDF" to start the conversion

## Project Structure

```
Hiel Converter Linux/
├── domain/                 # Domain layer (entities, value objects, interfaces)
│   ├── entities.py        # PDFDocument entity
│   ├── value_objects.py   # ConversionOptions and ConversionType
│   └── interfaces/        # Abstract base classes
├── infrastructure/        # Infrastructure layer (concrete implementations)
│   ├── pdf_repository_impl.py    # PDF operations implementation
│   ├── converter_factory.py      # Converter factory
│   └── converters/               # Format-specific converters
├── presentation/          # Presentation layer (UI components)
│   └── main_view.py      # Main application UI
├── use_cases/            # Application use cases
│   └── convert_pdf_use_case.py  # PDF conversion use case
├── config/               # Configuration management
│   └── app_config.py     # Application configuration
├── tests/                # Test files
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Dependencies

- **Flet** - Modern UI framework
- **PyPDF** - PDF processing
- **pdf2image** - PDF to image conversion
- **Pillow** - Image processing
- **pypandoc** - Document conversion (requires Pandoc)
- **python-docx** - Word document handling
- **reportlab** - PDF generation and manipulation

## Configuration

The application creates a configuration file at `~/.hiel_converter/config.json` with user preferences:

- Window size and position
- Default output directory
- Last used directories
- Conversion settings
- Logging configuration

## Error Handling

The application includes comprehensive error handling:

- Invalid PDF file detection
- Missing dependency warnings
- Conversion failure notifications
- User-friendly error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the clean architecture patterns
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the logs in `~/.hiel_converter/app.log`
- Ensure all dependencies are properly installed
- Verify Pandoc is installed for document format conversions

## Troubleshooting

**Common Issues:**

1. **Pandoc not found**: Install Pandoc for Word/HTML/Markdown conversion
2. **PDF won't load**: Ensure the PDF file is not corrupted or encrypted
3. **Conversion fails**: Check the application logs for detailed error messages
4. **UI not responding**: Ensure all Python dependencies are installed in the virtual environment

**System Requirements:**
- Python 3.8 or higher
- 2GB RAM minimum
- 100MB disk space for installation
- Additional space for converted files