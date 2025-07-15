"""
Factory for creating PDF converters based on conversion type.
"""

from typing import Dict, Type
from domain.interfaces.converter import Converter
from domain.value_objects import ConversionType, ConversionOptions
from infrastructure.converters.word_converter import WordConverter
from infrastructure.converters.text_converter import TextConverter
from infrastructure.converters.html_converter import HtmlConverter
from infrastructure.converters.markdown_converter import MarkdownConverter
from infrastructure.converters.image_converter import ImageConverter


class ConverterFactory:
    """
    Factory class for creating appropriate converter instances based on conversion type.
    """
    
    def __init__(self):
        """Initialize the converter factory with available converters."""
        self._converters: Dict[ConversionType, Type[Converter]] = {
            ConversionType.WORD: WordConverter,
            ConversionType.TEXT: TextConverter,
            ConversionType.HTML: HtmlConverter,
            ConversionType.MARKDOWN: MarkdownConverter,
            ConversionType.IMAGE: ImageConverter,
        }
    
    def create_converter(self, conversion_type: ConversionType) -> Converter:
        """
        Create a converter instance for the specified conversion type.
        
        Args:
            conversion_type: The type of conversion to perform
            
        Returns:
            Converter instance for the specified type
            
        Raises:
            ValueError: If the conversion type is not supported
        """
        if conversion_type not in self._converters:
            supported_types = ', '.join([t.value for t in self._converters.keys()])
            raise ValueError(f"Conversion type '{conversion_type.value}' is not supported. "
                           f"Supported types: {supported_types}")
        
        converter_class = self._converters[conversion_type]
        return converter_class()
    
    def get_supported_types(self) -> list[ConversionType]:
        """
        Get list of supported conversion types.
        
        Returns:
            List of supported ConversionType enum values
        """
        return list(self._converters.keys())
    
    def is_supported(self, conversion_type: ConversionType) -> bool:
        """
        Check if a conversion type is supported.
        
        Args:
            conversion_type: The conversion type to check
            
        Returns:
            True if the conversion type is supported, False otherwise
        """
        return conversion_type in self._converters
    
    def validate_conversion(self, options: ConversionOptions) -> bool:
        """
        Validate if a conversion can be performed with the given options.
        
        Args:
            options: ConversionOptions specifying the conversion details
            
        Returns:
            True if the conversion can be performed, False otherwise
        """
        if not self.is_supported(options.type):
            return False
        
        try:
            converter = self.create_converter(options.type)
            return converter.validate_conversion(options)
        except Exception:
            return False