"""
HTML converter implementation.
"""

from pathlib import Path
from typing import Any
import logging
import pypandoc

from domain.interfaces.converter import Converter
from domain.entities import PDFDocument
from domain.value_objects import ConversionOptions, ConversionType


class HtmlConverter(Converter):
    """
    Converter for converting PDFs to HTML format.
    """
    
    def __init__(self):
        """Initialize the HTML converter."""
        self.logger = logging.getLogger(__name__)
    
    def convert(self, document: PDFDocument, options: ConversionOptions) -> Path:
        """
        Convert a PDF document to HTML format.
        
        Args:
            document: PDFDocument instance to convert
            options: ConversionOptions specifying the conversion details
            
        Returns:
            Path to the converted HTML file
            
        Raises:
            ValueError: If the conversion cannot be performed
        """
        if not self.validate_conversion(options):
            raise ValueError("Invalid conversion options for HTML conversion")
        
        try:
            # Ensure output directory exists
            options.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Set output path with .html extension
            output_path = options.output_path
            if not output_path.suffix:
                output_path = output_path.with_suffix('.html')
            
            # Convert PDF to HTML using pypandoc
            pypandoc.convert_file(
                str(document.path),
                'html',
                outputfile=str(output_path),
                extra_args=[
                    '--extract-media', str(output_path.parent / 'media'),
                    '--standalone',
                    '--self-contained'
                ]
            )
            
            self.logger.info(f"Successfully converted PDF to HTML: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to convert PDF to HTML: {str(e)}")
            raise ValueError(f"HTML conversion failed: {str(e)}")
    
    def validate_conversion(self, options: ConversionOptions) -> bool:
        """
        Validate if a conversion can be performed with the given options.
        
        Args:
            options: ConversionOptions specifying the conversion details
            
        Returns:
            True if the conversion can be performed, False otherwise
        """
        try:
            # Check if conversion type is correct
            if options.type != ConversionType.HTML:
                return False
            
            # Check if output path is valid
            if not options.output_path.parent.exists():
                return False
            
            # Check if pypandoc is available
            try:
                pypandoc.get_pandoc_version()
            except OSError:
                self.logger.error("Pandoc is not installed or not accessible")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return False