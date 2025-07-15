#!/usr/bin/env python3
"""
Quick test script to verify image conversion is working.
"""

import sys
from pathlib import Path
from domain.entities import PDFDocument
from domain.value_objects import ConversionOptions, ConversionType
from infrastructure.pdf_repository_impl import PDFRepositoryImpl
from infrastructure.converters.image_converter import ImageConverter

def test_image_conversion():
    """Test image conversion functionality."""
    print("Testing image conversion...")
    
    # Check if we have a PDF file to test with
    test_files = [
        Path("/home/serhabdel/Documents/Social Media Agevolami/Morocco Agevolami/week 14-07-25/MOROCCO-FREE-ZONES-PART-3.pdf"),
        Path("test.pdf"),
        Path("sample.pdf")
    ]
    
    pdf_file = None
    for test_file in test_files:
        if test_file.exists():
            pdf_file = test_file
            break
    
    if not pdf_file:
        print("❌ No test PDF file found. Please provide a PDF file to test.")
        return False
    
    try:
        # Initialize components
        repo = PDFRepositoryImpl()
        converter = ImageConverter()
        
        # Load PDF
        print(f"📄 Loading PDF: {pdf_file}")
        document = repo.load_pdf(pdf_file)
        print(f"✅ PDF loaded successfully: {document.pages} pages")
        
        # Test different quality settings
        qualities = ["low", "medium", "high"]
        
        for quality in qualities:
            print(f"\n🔄 Testing {quality} quality conversion...")
            
            # Create output directory
            output_dir = Path(f"/tmp/test_conversion_{quality}")
            output_dir.mkdir(exist_ok=True)
            
            # Create conversion options
            options = ConversionOptions(
                type=ConversionType.IMAGE,
                output_path=output_dir,
                image_quality=quality
            )
            
            # Convert
            result_path = converter.convert(document, options)
            
            # Check results
            image_files = list(result_path.glob("*.jpg")) + list(result_path.glob("*.png"))
            total_size = sum(f.stat().st_size for f in image_files)
            
            print(f"✅ {quality.capitalize()} conversion successful!")
            print(f"   📁 Output: {result_path}")
            print(f"   📊 Files: {len(image_files)}")
            print(f"   💾 Total size: {total_size / (1024*1024):.2f} MB")
        
        print(f"\n🎉 All image conversion tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Image conversion test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_image_conversion()
    sys.exit(0 if success else 1)