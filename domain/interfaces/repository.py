"""
Abstract base class for PDF repository operations.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from pathlib import Path

from ..entities import PDFDocument


class PDFRepository(ABC):
    """
    Abstract base class for PDF document repository operations.
    
    This interface defines the contract for storing, retrieving, and managing
    PDF documents in the system.
    """
    
    @abstractmethod
    def load_pdf(self, file_path: Path) -> PDFDocument:
        """
        Load a PDF document from a file path.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            PDFDocument instance with loaded metadata and page count
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF
            PermissionError: If the file cannot be read
        """
        pass
    
    @abstractmethod
    def save_pdf(self, document: PDFDocument, output_path: Path) -> None:
        """
        Save a PDF document to a file path.
        
        Args:
            document: PDFDocument instance to save
            output_path: Path where the PDF should be saved
            
        Raises:
            PermissionError: If the file cannot be written
            ValueError: If the document is invalid
        """
        pass
    
    @abstractmethod
    def get_pdf_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF metadata (title, author, creation_date, etc.)
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF
        """
        pass
    
    @abstractmethod
    def get_page_count(self, file_path: Path) -> int:
        """
        Get the number of pages in a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF
        """
        pass
    
    @abstractmethod
    def is_pdf_encrypted(self, file_path: Path) -> bool:
        """
        Check if a PDF file is encrypted/password protected.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            True if the PDF is encrypted, False otherwise
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF
        """
        pass
    
    @abstractmethod
    def validate_pdf(self, file_path: Path) -> bool:
        """
        Validate if a file is a valid PDF.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if the file is a valid PDF, False otherwise
        """
        pass
    
    @abstractmethod
    def get_pdf_pages(self, file_path: Path, page_range: Optional[List[int]] = None) -> List[bytes]:
        """
        Extract specific pages from a PDF as image bytes.
        
        Args:
            file_path: Path to the PDF file
            page_range: List of page numbers to extract (1-based). If None, extract all pages
            
        Returns:
            List of bytes representing each page as an image
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF or page range is invalid
        """
        pass
    
    @abstractmethod
    def merge_pdfs(self, pdf_paths: List[Path], output_path: Path) -> None:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            pdf_paths: List of PDF file paths to merge
            output_path: Path where the merged PDF should be saved
            
        Raises:
            FileNotFoundError: If any PDF file doesn't exist
            ValueError: If any file is not a valid PDF
            PermissionError: If files cannot be read or output cannot be written
        """
        pass
    
    @abstractmethod
    def split_pdf(self, file_path: Path, output_directory: Path, pages_per_split: int = 1) -> List[Path]:
        """
        Split a PDF file into multiple smaller PDFs.
        
        Args:
            file_path: Path to the PDF file to split
            output_directory: Directory where split PDFs should be saved
            pages_per_split: Number of pages per split file
            
        Returns:
            List of paths to the created split PDF files
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            ValueError: If the file is not a valid PDF or parameters are invalid
            PermissionError: If files cannot be read or written
        """
        pass
