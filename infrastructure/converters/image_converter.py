"""
Image converter implementation with size optimization.
"""

from pathlib import Path
from typing import Any, Dict, Tuple
import logging
from pdf2image import convert_from_path
from PIL import Image
import os

from domain.interfaces.converter import Converter
from domain.entities import PDFDocument
from domain.value_objects import ConversionOptions, ConversionType


class ImageConverter(Converter):
    """
    Converter for converting PDFs to image format with size optimization.
    """
    
    def __init__(self):
        """Initialize the image converter."""
        self.logger = logging.getLogger(__name__)
        
        # Default optimization settings
        self.optimization_settings = {
            'dpi': 150,  # Reduced from 300 for smaller files
            'format': 'JPEG',  # JPEG is much smaller than PNG
            'quality': 85,  # Good balance between quality and size
            'optimize': True,  # Enable PIL optimization
            'progressive': True,  # Progressive JPEG for better compression
        }
        
        # Quality presets
        self.quality_presets = {
            'low': {'dpi': 72, 'quality': 60, 'format': 'JPEG'},
            'medium': {'dpi': 150, 'quality': 85, 'format': 'JPEG'},
            'high': {'dpi': 200, 'quality': 95, 'format': 'JPEG'},
            'ultra': {'dpi': 300, 'quality': 95, 'format': 'PNG'},
        }
    
    def convert(self, document: PDFDocument, options: ConversionOptions) -> Path:
        """
        Convert a PDF document to optimized image format.
        
        Args:
            document: PDFDocument instance to convert
            options: ConversionOptions specifying the conversion details
            
        Returns:
            Path to the directory containing converted images
            
        Raises:
            ValueError: If the conversion cannot be performed
        """
        if not self.validate_conversion(options):
            raise ValueError("Invalid conversion options for image conversion")
        
        try:
            # Ensure output directory exists
            output_dir = options.output_path
            if output_dir.suffix:
                # If output_path has an extension, use its parent as directory
                output_dir = output_dir.parent
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Get optimization settings
            settings = self._get_optimization_settings(options)
            
            # Convert PDF to images with optimized settings
            images = convert_from_path(
                str(document.path),
                dpi=settings['dpi'],
                fmt='RGB'  # Use RGB for better JPEG compression
            )
            
            # Save each page as optimized image
            image_paths = []
            base_name = document.path.stem
            file_extension = '.jpg' if settings['format'] == 'JPEG' else '.png'
            
            total_original_size = 0
            total_optimized_size = 0
            
            for i, image in enumerate(images, 1):
                image_filename = f"{base_name}_page_{i:03d}{file_extension}"
                image_path = output_dir / image_filename
                
                # Calculate original size (approximate)
                original_size = image.size[0] * image.size[1] * 3  # RGB bytes
                total_original_size += original_size
                
                # Save with optimization
                optimized_image = self._optimize_image(image, settings)
                optimized_image.save(
                    image_path,
                    settings['format'],
                    quality=settings.get('quality', 85),
                    optimize=settings.get('optimize', True),
                    progressive=settings.get('progressive', True)
                )
                
                # Calculate actual file size
                file_size = os.path.getsize(image_path)
                total_optimized_size += file_size
                
                image_paths.append(image_path)
            
            # Log compression statistics
            compression_ratio = (1 - total_optimized_size / total_original_size) * 100
            self.logger.info(f"Successfully converted PDF to {len(images)} images in: {output_dir}")
            self.logger.info(f"Compression: {compression_ratio:.1f}% size reduction")
            self.logger.info(f"Total size: {total_optimized_size / (1024*1024):.2f} MB")
            
            # Return the directory containing the images
            return output_dir
            
        except Exception as e:
            self.logger.error(f"Failed to convert PDF to images: {str(e)}")
            
            # Provide more specific error messages
            error_msg = str(e)
            if "Resampling" in error_msg:
                error_msg = "PIL version compatibility issue. Please check Pillow installation."
            elif "convert_from_path" in error_msg:
                error_msg = "PDF to image conversion failed. Check if poppler-utils is installed."
            elif "No such file" in error_msg:
                error_msg = "PDF file not found or inaccessible."
            elif "permission" in error_msg.lower():
                error_msg = "Permission denied. Check file permissions."
            
            raise ValueError(f"Image conversion failed: {error_msg}")
    
    def _get_optimization_settings(self, options: ConversionOptions) -> Dict[str, Any]:
        """
        Get optimization settings based on conversion options.
        
        Args:
            options: ConversionOptions specifying the conversion details
            
        Returns:
            Dictionary containing optimization settings
        """
        # Default to medium quality for best balance
        settings = self.quality_presets['medium'].copy()
        
        # Override with custom settings from options if available
        # This allows for future extension of ConversionOptions
        if hasattr(options, 'image_quality'):
            if options.image_quality in self.quality_presets:
                settings.update(self.quality_presets[options.image_quality])
        
        if hasattr(options, 'image_dpi'):
            settings['dpi'] = options.image_dpi
        
        if hasattr(options, 'image_format'):
            settings['format'] = options.image_format
        
        if hasattr(options, 'image_compression_quality'):
            settings['quality'] = options.image_compression_quality
        
        return settings
    
    def _optimize_image(self, image: Image.Image, settings: Dict[str, Any]) -> Image.Image:
        """
        Optimize image for size reduction while maintaining quality.
        
        Args:
            image: PIL Image to optimize
            settings: Optimization settings
            
        Returns:
            Optimized PIL Image
        """
        # Convert to RGB if saving as JPEG
        if settings['format'] == 'JPEG' and image.mode in ('RGBA', 'LA', 'P'):
            # Create white background for transparency
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Resize if image is too large (optional size limit)
        max_dimension = 2048  # Maximum width or height
        if max(image.size) > max_dimension:
            ratio = max_dimension / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            
            # Handle different PIL versions for resampling
            try:
                # Try new Pillow version (>= 10.0.0)
                resample_filter = Image.Resampling.LANCZOS
            except AttributeError:
                # Fall back to older Pillow version
                resample_filter = Image.LANCZOS
            
            image = image.resize(new_size, resample_filter)
            self.logger.info(f"Resized image to {new_size} for size optimization")
        
        return image
    
    def get_estimated_file_size(self, document: PDFDocument, options: ConversionOptions) -> Tuple[int, str]:
        """
        Estimate the total file size for the conversion.
        
        Args:
            document: PDFDocument to convert
            options: ConversionOptions specifying the conversion details
            
        Returns:
            Tuple of (estimated_size_bytes, formatted_size_string)
        """
        settings = self._get_optimization_settings(options)
        
        # Rough estimation based on DPI and format
        pages = document.pages
        
        if settings['format'] == 'JPEG':
            # JPEG: approximately 200-800 KB per page depending on DPI and quality
            size_per_page = {
                72: 150_000,   # ~150 KB
                150: 400_000,  # ~400 KB
                200: 700_000,  # ~700 KB
                300: 1_200_000 # ~1.2 MB
            }
        else:  # PNG
            # PNG: approximately 500KB-3MB per page depending on DPI
            size_per_page = {
                72: 500_000,   # ~500 KB
                150: 1_000_000, # ~1 MB
                200: 2_000_000, # ~2 MB
                300: 3_000_000  # ~3 MB
            }
        
        dpi = settings['dpi']
        base_size = size_per_page.get(dpi, size_per_page[150])
        
        # Adjust for quality
        if settings['format'] == 'JPEG':
            quality_factor = settings.get('quality', 85) / 85.0
            base_size = int(base_size * quality_factor)
        
        total_size = base_size * pages
        
        # Format size string
        if total_size < 1024:
            size_str = f"{total_size} B"
        elif total_size < 1024 * 1024:
            size_str = f"{total_size / 1024:.1f} KB"
        else:
            size_str = f"{total_size / (1024 * 1024):.1f} MB"
        
        return total_size, size_str
    
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
            if options.type != ConversionType.IMAGE:
                return False
            
            # Check if output path is valid
            output_dir = options.output_path
            if output_dir.suffix:
                output_dir = output_dir.parent
            
            if not output_dir.exists():
                try:
                    output_dir.mkdir(parents=True, exist_ok=True)
                except Exception:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return False