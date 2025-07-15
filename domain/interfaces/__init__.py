"""
Domain interfaces - abstract base classes for repositories and services.
"""

from .repository import PDFRepository
from .converter import Converter
from .security import SecurityService

__all__ = ['PDFRepository', 'Converter', 'SecurityService']
