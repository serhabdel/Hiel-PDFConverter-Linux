"""
Text converter implementation.
"""

from pathlib import Path
from typing import Any
import logging
import pypdf

from domain.interfaces.converter import Converter
from domain.entities import PDFDocument
from domain.value_objects import ConversionOptions, ConversionType


class TextConverter(Converter):
    """
    Converter for converting PDFs to plain text.
    """
    
    def __init__(self):
        """Initialize the text converter."""
        self.logger = logging.getLogger(__name__)
    
    def convert(self, document: PDFDocument, options: ConversionOptions) -> Path:
        """
        Convert a PDF document to plain text.
        
        Args:
            document: PDFDocument instance to convert
            options: ConversionOptions specifying the conversion details
            
        Returns:
            Path to the converted text file
            
        Raises:
            ValueError: If the conversion cannot be performed
        """
        if not self.validate_conversion(options):
            raise ValueError("Invalid conversion options for text conversion")
        
        try:
            # Ensure output directory exists
            options.output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Set output path with .txt extension
            output_path = options.output_path
            if not output_path.suffix:
                output_path = output_path.with_suffix('.txt')
            
            # Extract text from PDF
            text_content = self._extract_text_from_pdf(document.path)
            
            # Write text to file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(text_content)
            
            self.logger.info(f"Successfully converted PDF to text: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to convert PDF to text: {str(e)}")
            raise ValueError(f"Text conversion failed: {str(e)}")
    
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
            if options.type != ConversionType.TEXT:
                return False
            
            # Check if output path is valid
            if not options.output_path.parent.exists():
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return False
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
        """
        try:
            text_content = []
            
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text.strip():
                            text_content.append(f"--- Page {page_num} ---\n")
                            text_content.append(page_text)
                            text_content.append("\n\n")
                    except Exception as e:
                        self.logger.warning(f"Could not extract text from page {page_num}: {str(e)}")
                        text_content.append(f"--- Page {page_num} ---\n")
                        text_content.append(f"[Error extracting text from this page: {str(e)}]\n\n")
            
            return "".join(text_content)
            
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            raise ValueError(f"Failed to extract text: {str(e)}")