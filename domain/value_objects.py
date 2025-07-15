"""
Domain value objects for the PDF converter application.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from pathlib import Path
from enum import Enum


class ConversionType(Enum):
    """Supported conversion types."""
    WORD = "word"
    EXCEL = "excel"
    POWERPOINT = "powerpoint"
    TEXT = "text"
    HTML = "html"
    MARKDOWN = "markdown"
    EPUB = "epub"
    RTF = "rtf"
    ODT = "odt"
    IMAGE = "image"


@dataclass(frozen=True)
class ConversionOptions:
    """
    Value object representing options for PDF conversion.
    Immutable to ensure consistency.
    """
    type: ConversionType
    output_path: Path
    permissions: Optional[Dict[str, bool]] = None
    password: Optional[str] = None
    image_quality: Optional[str] = None  # For image conversion: low, medium, high, ultra
    
    def __post_init__(self):
        """Validate conversion options after initialization."""
        if not isinstance(self.type, ConversionType):
            raise ValueError(f"Invalid conversion type: {self.type}")
        
        if not isinstance(self.output_path, Path):
            object.__setattr__(self, 'output_path', Path(self.output_path))
        
        # Validate output path directory exists
        if not self.output_path.parent.exists():
            raise ValueError(f"Output directory does not exist: {self.output_path.parent}")
        
        # Validate permissions if provided
        if self.permissions is not None:
            if not isinstance(self.permissions, dict):
                raise ValueError("Permissions must be a dictionary")
            
            valid_permissions = {
                'allow_printing', 'allow_copying', 'allow_modification',
                'allow_annotation', 'allow_form_filling', 'allow_extraction',
                'allow_assembly', 'allow_degraded_printing'
            }
            
            for permission in self.permissions.keys():
                if permission not in valid_permissions:
                    raise ValueError(f"Invalid permission: {permission}")
                
                if not isinstance(self.permissions[permission], bool):
                    raise ValueError(f"Permission value must be boolean: {permission}")
        
        # Validate password if provided
        if self.password is not None and not isinstance(self.password, str):
            raise ValueError("Password must be a string")
        
        # Validate image quality if provided
        if self.image_quality is not None:
            valid_qualities = {'low', 'medium', 'high', 'ultra'}
            if self.image_quality not in valid_qualities:
                raise ValueError(f"Invalid image quality: {self.image_quality}. Must be one of: {valid_qualities}")
    
    @property
    def file_extension(self) -> str:
        """Get the appropriate file extension for the conversion type."""
        extension_map = {
            ConversionType.WORD: ".docx",
            ConversionType.EXCEL: ".xlsx",
            ConversionType.POWERPOINT: ".pptx",
            ConversionType.TEXT: ".txt",
            ConversionType.HTML: ".html",
            ConversionType.MARKDOWN: ".md",
            ConversionType.EPUB: ".epub",
            ConversionType.RTF: ".rtf",
            ConversionType.ODT: ".odt",
            ConversionType.IMAGE: ".png",
        }
        return extension_map[self.type]
    
    @property
    def requires_password(self) -> bool:
        """Check if conversion requires a password."""
        return self.password is not None
    
    @property
    def has_permissions(self) -> bool:
        """Check if conversion has permission restrictions."""
        return self.permissions is not None and len(self.permissions) > 0
    
    def get_output_filename(self, base_name: str) -> str:
        """Generate output filename with appropriate extension."""
        if self.output_path.suffix:
            return self.output_path.name
        else:
            return f"{base_name}{self.file_extension}"
    
    def with_output_path(self, output_path: Path) -> 'ConversionOptions':
        """Create a new ConversionOptions with a different output path."""
        return ConversionOptions(
            type=self.type,
            output_path=output_path,
            permissions=self.permissions,
            password=self.password,
            image_quality=self.image_quality
        )
    
    def with_password(self, password: str) -> 'ConversionOptions':
        """Create a new ConversionOptions with a password."""
        return ConversionOptions(
            type=self.type,
            output_path=self.output_path,
            permissions=self.permissions,
            password=password,
            image_quality=self.image_quality
        )
    
    def with_image_quality(self, image_quality: str) -> 'ConversionOptions':
        """Create a new ConversionOptions with image quality settings."""
        return ConversionOptions(
            type=self.type,
            output_path=self.output_path,
            permissions=self.permissions,
            password=self.password,
            image_quality=image_quality
        )
    
    def __str__(self) -> str:
        return f"ConversionOptions(type={self.type.value}, output_path={self.output_path})"
    
    def __repr__(self) -> str:
        return self.__str__()
