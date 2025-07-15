"""
Domain entities for the PDF converter application.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime


@dataclass
class PDFDocument:
    """
    PDF document entity representing a PDF file with its metadata and pages.
    """
    path: Path
    pages: int
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """Validate the PDF document data after initialization."""
        if not isinstance(self.path, Path):
            self.path = Path(self.path)
        
        if not self.path.exists():
            raise ValueError(f"PDF file does not exist: {self.path}")
        
        if not self.path.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {self.path}")
        
        if self.pages <= 0:
            raise ValueError("PDF must have at least one page")
        
        if not isinstance(self.metadata, dict):
            raise ValueError("Metadata must be a dictionary")
    
    @property
    def filename(self) -> str:
        """Get the filename of the PDF document."""
        return self.path.name
    
    @property
    def size(self) -> int:
        """Get the size of the PDF file in bytes."""
        return self.path.stat().st_size
    
    @property
    def title(self) -> Optional[str]:
        """Get the title from metadata if available."""
        return self.metadata.get('title')
    
    @property
    def author(self) -> Optional[str]:
        """Get the author from metadata if available."""
        return self.metadata.get('author')
    
    @property
    def creation_date(self) -> Optional[datetime]:
        """Get the creation date from metadata if available."""
        return self.metadata.get('creation_date')
    
    def __str__(self) -> str:
        return f"PDFDocument(path={self.path}, pages={self.pages})"
    
    def __repr__(self) -> str:
        return self.__str__()
