"""
Use case for converting PDF documents.
"""

from pathlib import Path
from typing import Any
import logging

from domain.entities import PDFDocument
from domain.value_objects import ConversionOptions
from domain.interfaces.repository import PDFRepository
from infrastructure.converter_factory import ConverterFactory


class ConvertPDFUseCase:
    """
    Use case for converting PDF documents to various formats.
    """
    
    def __init__(self, pdf_repository: PDFRepository, converter_factory: ConverterFactory):
        """
        Initialize the convert PDF use case.
        
        Args:
            pdf_repository: Repository for PDF operations
            converter_factory: Factory for creating converters
        """
        self.pdf_repository = pdf_repository
        self.converter_factory = converter_factory
        self.logger = logging.getLogger(__name__)
    
    def execute(self, document: PDFDocument, options: ConversionOptions) -> Path:
        """
        Execute the PDF conversion use case.
        
        Args:
            document: PDFDocument to convert
            options: ConversionOptions specifying conversion details
            
        Returns:
            Path to the converted file or directory
            
        Raises:
            ValueError: If conversion fails or options are invalid
        """
        try:
            self.logger.info(f"Starting conversion of {document.filename} to {options.type.value}")
            
            # Validate document
            if not document.path.exists():
                raise ValueError(f"Source PDF file not found: {document.path}")
            
            # Validate conversion options
            if not self.converter_factory.validate_conversion(options):
                raise ValueError("Invalid conversion options")
            
            # Create converter
            converter = self.converter_factory.create_converter(options.type)
            
            # Perform conversion
            result_path = converter.convert(document, options)
            
            self.logger.info(f"Successfully converted {document.filename} to {result_path}")
            return result_path
            
        except Exception as e:
            self.logger.error(f"Conversion failed: {str(e)}")
            raise ValueError(f"Conversion failed: {str(e)}")
    
    def validate_conversion(self, document: PDFDocument, options: ConversionOptions) -> bool:
        """
        Validate if a conversion can be performed.
        
        Args:
            document: PDFDocument to convert
            options: ConversionOptions specifying conversion details
            
        Returns:
            True if conversion is valid, False otherwise
        """
        try:
            # Check if document exists
            if not document.path.exists():
                return False
            
            # Check if conversion type is supported
            if not self.converter_factory.is_supported(options.type):
                return False
            
            # Validate conversion options
            return self.converter_factory.validate_conversion(options)
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return False
    
    def get_supported_formats(self) -> list[str]:
        """
        Get list of supported conversion formats.
        
        Returns:
            List of supported format names
        """
        return [conv_type.value for conv_type in self.converter_factory.get_supported_types()]