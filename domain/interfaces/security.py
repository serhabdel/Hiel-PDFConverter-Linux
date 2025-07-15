"""
Abstract base class for PDF security operations.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

from ..entities import PDFDocument


class SecurityService(ABC):
    """
    Abstract base class for PDF security operations.
    
    This interface defines the contract for handling PDF security features
    such as encryption, password protection, and permission management.
    """
    
    @abstractmethod
    def encrypt_pdf(self, document: PDFDocument, password: str, permissions: Optional[Dict[str, bool]] = None) -> PDFDocument:
        """
        Encrypt a PDF document with a password and optional permissions.
        
        Args:
            document: PDFDocument instance to encrypt
            password: Password to encrypt the PDF with
            permissions: Optional dictionary of permissions to set
            
        Returns:
            Encrypted PDFDocument instance
            
        Raises:
            ValueError: If encryption fails or invalid parameters provided
        """
        pass
    
    @abstractmethod
    def decrypt_pdf(self, document: PDFDocument, password: str) -> PDFDocument:
        """
        Decrypt a password-protected PDF document.
        
        Args:
            document: Encrypted PDFDocument instance
            password: Password to decrypt the PDF with
            
        Returns:
            Decrypted PDFDocument instance
            
        Raises:
            ValueError: If decryption fails or password is incorrect
        """
        pass
    
    @abstractmethod
    def verify_password(self, document: PDFDocument, password: str) -> bool:
        """
        Verify if a password is correct for an encrypted PDF.
        
        Args:
            document: Encrypted PDFDocument instance
            password: Password to verify
            
        Returns:
            True if password is correct, False otherwise
        """
        pass
    
    @abstractmethod
    def get_permissions(self, document: PDFDocument) -> Dict[str, bool]:
        """
        Get the current permissions for a PDF document.
        
        Args:
            document: PDFDocument instance
            
        Returns:
            Dictionary containing current permissions
        """
        pass
    
    @abstractmethod
    def set_permissions(self, document: PDFDocument, permissions: Dict[str, bool]) -> PDFDocument:
        """
        Set permissions for a PDF document.
        
        Args:
            document: PDFDocument instance
            permissions: Dictionary of permissions to set
            
        Returns:
            PDFDocument instance with updated permissions
            
        Raises:
            ValueError: If permissions are invalid
        """
        pass
    
    @abstractmethod
    def remove_password(self, document: PDFDocument, password: str) -> PDFDocument:
        """
        Remove password protection from a PDF document.
        
        Args:
            document: Encrypted PDFDocument instance
            password: Current password
            
        Returns:
            Unencrypted PDFDocument instance
            
        Raises:
            ValueError: If password is incorrect or removal fails
        """
        pass
    
    @abstractmethod
    def is_encrypted(self, document: PDFDocument) -> bool:
        """
        Check if a PDF document is encrypted.
        
        Args:
            document: PDFDocument instance to check
            
        Returns:
            True if the document is encrypted, False otherwise
        """
        pass
    
    @abstractmethod
    def can_extract_text(self, document: PDFDocument) -> bool:
        """
        Check if text extraction is allowed for a PDF document.
        
        Args:
            document: PDFDocument instance to check
            
        Returns:
            True if text extraction is allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def can_print(self, document: PDFDocument) -> bool:
        """
        Check if printing is allowed for a PDF document.
        
        Args:
            document: PDFDocument instance to check
            
        Returns:
            True if printing is allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def can_copy(self, document: PDFDocument) -> bool:
        """
        Check if copying is allowed for a PDF document.
        
        Args:
            document: PDFDocument instance to check
            
        Returns:
            True if copying is allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def can_modify(self, document: PDFDocument) -> bool:
        """
        Check if modification is allowed for a PDF document.
        
        Args:
            document: PDFDocument instance to check
            
        Returns:
            True if modification is allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def validate_permissions(self, permissions: Dict[str, bool]) -> bool:
        """
        Validate if the provided permissions are valid.
        
        Args:
            permissions: Dictionary of permissions to validate
            
        Returns:
            True if permissions are valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_security_info(self, document: PDFDocument) -> Dict[str, Any]:
        """
        Get comprehensive security information for a PDF document.
        
        Args:
            document: PDFDocument instance
            
        Returns:
            Dictionary containing security information (encryption, permissions, etc.)
        """
        pass
