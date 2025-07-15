"""
Abstract base class for PDF conversion operations.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..value_objects import ConversionOptions
from ..entities import PDFDocument


class Converter(ABC):
    """
    Abstract base class for PDF conversion operations.
    
    This interface defines the contract for converting PDF documents
    into various other formats.
    """
    
    @abstractmethod
    def convert(self, document: PDFDocument, options: ConversionOptions) -> Any:
        """
        Convert a PDF document into another format.
        
        Args:
            document: PDFDocument instance to convert
            options: ConversionOptions specifying the conversion details
            
        Returns:
            Converted data in the format specified by options
            
        Raises:
            ValueError: If the conversion cannot be performed
        """
        pass
    
    @abstractmethod
    def validate_conversion(self, options: ConversionOptions) -> bool:
        """
        Validate if a conversion can be performed with the given options.
        
        Args:
            options: ConversionOptions specifying the conversion details
            
        Returns:
            True if the conversion can be performed, False otherwise
        """
        pass

