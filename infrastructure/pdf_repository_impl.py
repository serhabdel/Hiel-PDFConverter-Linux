"""
Concrete implementation of PDF repository operations.
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import pypdf
from pdf2image import convert_from_path
import logging

from domain.entities import PDFDocument
from domain.interfaces.repository import PDFRepository


class PDFRepositoryImpl(PDFRepository):
    """
    Concrete implementation of PDF repository using PyPDF and pdf2image.
    """
    
    def __init__(self):
        """Initialize the PDF repository."""
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    
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
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"PDF file does not exist: {file_path}")
            
            if not self.validate_pdf(file_path):
                raise ValueError(f"File is not a valid PDF: {file_path}")
            
            # Get metadata and page count
            metadata = self.get_pdf_metadata(file_path)
            page_count = self.get_page_count(file_path)
            
            return PDFDocument(
                path=file_path,
                pages=page_count,
                metadata=metadata
            )
            
        except PermissionError:
            raise PermissionError(f"Cannot read PDF file: {file_path}")
        except Exception as e:
            self.logger.error(f"Error loading PDF {file_path}: {str(e)}")
            raise ValueError(f"Failed to load PDF: {str(e)}")
    
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
        try:
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy the original file to the new location
            import shutil
            shutil.copy2(document.path, output_path)
            
            self.logger.info(f"PDF saved to: {output_path}")
            
        except PermissionError:
            raise PermissionError(f"Cannot write to path: {output_path}")
        except Exception as e:
            raise ValueError(f"Failed to save PDF: {str(e)}")
    
    def get_pdf_metadata(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF metadata
        """
        metadata = {}
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                if pdf_reader.metadata:
                    metadata = {
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'subject': pdf_reader.metadata.get('/Subject', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'producer': pdf_reader.metadata.get('/Producer', ''),
                        'creation_date': pdf_reader.metadata.get('/CreationDate'),
                        'modification_date': pdf_reader.metadata.get('/ModDate'),
                    }
                    
                    # Clean up None values
                    metadata = {k: v for k, v in metadata.items() if v is not None}
                
        except Exception as e:
            self.logger.warning(f"Could not extract metadata from {file_path}: {str(e)}")
            
        return metadata
    
    def get_page_count(self, file_path: Path) -> int:
        """
        Get the number of pages in a PDF file.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Number of pages in the PDF
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                return len(pdf_reader.pages)
                
        except Exception as e:
            self.logger.error(f"Could not get page count from {file_path}: {str(e)}")
            raise ValueError(f"Failed to get page count: {str(e)}")
    
    def is_pdf_encrypted(self, file_path: Path) -> bool:
        """
        Check if a PDF file is encrypted/password protected.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            True if the PDF is encrypted, False otherwise
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                return pdf_reader.is_encrypted
                
        except Exception as e:
            self.logger.error(f"Could not check encryption status of {file_path}: {str(e)}")
            return False
    
    def validate_pdf(self, file_path: Path) -> bool:
        """
        Validate if a file is a valid PDF.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if the file is a valid PDF, False otherwise
        """
        try:
            if not file_path.exists():
                return False
                
            if not file_path.suffix.lower() == '.pdf':
                return False
                
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                # Try to access pages to ensure it's a valid PDF
                len(pdf_reader.pages)
                return True
                
        except Exception:
            return False
    
    def get_pdf_pages(self, file_path: Path, page_range: Optional[List[int]] = None) -> List[bytes]:
        """
        Extract specific pages from a PDF as image bytes.
        
        Args:
            file_path: Path to the PDF file
            page_range: List of page numbers to extract (1-based)
            
        Returns:
            List of bytes representing each page as an image
        """
        try:
            images = convert_from_path(
                file_path,
                first_page=page_range[0] if page_range else None,
                last_page=page_range[-1] if page_range else None,
                dpi=200,
                fmt='PNG'
            )
            
            page_bytes = []
            for image in images:
                import io
                img_bytes = io.BytesIO()
                image.save(img_bytes, format='PNG')
                page_bytes.append(img_bytes.getvalue())
                
            return page_bytes
            
        except Exception as e:
            self.logger.error(f"Could not extract pages from {file_path}: {str(e)}")
            raise ValueError(f"Failed to extract pages: {str(e)}")
    
    def merge_pdfs(self, pdf_paths: List[Path], output_path: Path) -> None:
        """
        Merge multiple PDF files into a single PDF.
        
        Args:
            pdf_paths: List of PDF file paths to merge
            output_path: Path where the merged PDF should be saved
        """
        try:
            pdf_writer = pypdf.PdfWriter()
            
            for pdf_path in pdf_paths:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = pypdf.PdfReader(file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                
            self.logger.info(f"Merged {len(pdf_paths)} PDFs into: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Could not merge PDFs: {str(e)}")
            raise ValueError(f"Failed to merge PDFs: {str(e)}")
    
    def split_pdf(self, file_path: Path, output_directory: Path, pages_per_split: int = 1) -> List[Path]:
        """
        Split a PDF file into multiple smaller PDFs.
        
        Args:
            file_path: Path to the PDF file to split
            output_directory: Directory where split PDFs should be saved
            pages_per_split: Number of pages per split file
            
        Returns:
            List of paths to the created split PDF files
        """
        try:
            # Ensure output directory exists
            output_directory.mkdir(parents=True, exist_ok=True)
            
            split_files = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for start_page in range(0, total_pages, pages_per_split):
                    pdf_writer = pypdf.PdfWriter()
                    
                    # Add pages to the writer
                    end_page = min(start_page + pages_per_split, total_pages)
                    for page_num in range(start_page, end_page):
                        pdf_writer.add_page(pdf_reader.pages[page_num])
                    
                    # Create output filename
                    base_name = file_path.stem
                    output_filename = f"{base_name}_part_{start_page + 1:03d}-{end_page:03d}.pdf"
                    output_path = output_directory / output_filename
                    
                    # Write the split PDF
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                        
                    split_files.append(output_path)
                    
            self.logger.info(f"Split PDF into {len(split_files)} files")
            return split_files
            
        except Exception as e:
            self.logger.error(f"Could not split PDF {file_path}: {str(e)}")
            raise ValueError(f"Failed to split PDF: {str(e)}")