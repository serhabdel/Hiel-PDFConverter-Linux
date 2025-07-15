"""
Markdown converter implementation.
"""

from pathlib import Path
from typing import Any
import logging
import pypandoc

from domain.interfaces.converter import Converter
from domain.entities import PDFDocument
from domain.value_objects import ConversionOptions, ConversionType


class MarkdownConverter(Converter):
    """
    Converter for converting PDFs to Markdown format.
    """
    
    def __init__(self):
        """Initialize the Markdown converter."""
        self.logger = logging.getLogger(__name__)
    
    def convert(self, document: PDFDocument, options: ConversionOptions) -> Path:
        """
        Convert a PDF document to Markdown format.
        
        Args:
            document: PDFDocument instance to convert
            options: ConversionOptions specifying the conversion details
            
        Returns:
            Path to the converted Markdown file
            
        Raises:
            ValueError: If the conversion cannot be performed
        """
        if not self.validate_conversion(options):
            raise ValueError("Invalid conversion options for Markdown conversion")
        
        try:
            # Ensure output directory exists
            options.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Set output path with .md extension
            output_path = options.output_path
            if not output_path.suffix:
                output_path = output_path.with_suffix('.md')
            
            # Convert PDF to Markdown using pypandoc
            pypandoc.convert_file(
                str(document.path),
                'markdown',
                outputfile=str(output_path),
                extra_args=[
                    '--extract-media', str(output_path.parent / 'media'),
                    '--wrap=none',
                    '--atx-headers'
                ]
            )
            
            self.logger.info(f"Successfully converted PDF to Markdown: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to convert PDF to Markdown: {str(e)}")
            raise ValueError(f"Markdown conversion failed: {str(e)}")
    
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
            if options.type != ConversionType.MARKDOWN:
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