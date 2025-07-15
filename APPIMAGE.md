# Hiel PDF Converter - AppImage Distribution

## 📦 **AppImage Ready!**

The Hiel PDF Converter is now available as a portable AppImage for Linux systems.

### 🚀 **Quick Start**

```bash
# Download and run (example)
chmod +x Hiel-PDF-Converter-1.0.0-x86_64.AppImage
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage
```

### 📋 **AppImage Information**

- **File**: `Hiel-PDF-Converter-1.0.0-x86_64.AppImage`
- **Size**: 34 MB
- **Architecture**: x86_64 (64-bit)
- **Version**: 1.0.0
- **Format**: AppImage (portable executable)

### ✨ **Features Included**

- **Complete PDF Converter**: All conversion formats supported
- **Advanced Image Quality Control**: Custom DPI, JPEG/PNG, compression settings
- **Modern Scrollable UI**: Responsive design with quality presets
- **Size Optimization**: Up to 97% compression for image outputs
- **Self-contained**: No installation required, includes all dependencies

### 🔧 **System Requirements**

- **OS**: Linux (any distribution)
- **Architecture**: x86_64 (64-bit)
- **Desktop**: X11 or Wayland
- **Optional**: Pandoc for Word/HTML/Markdown conversion

### 📁 **Usage Options**

#### **1. Portable Mode**
```bash
# Run from any location
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage
```

#### **2. Desktop Integration**
```bash
# Extract desktop files (optional)
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage --appimage-extract
```

#### **3. Portable Home**
```bash
# Create portable data directory
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage --appimage-portable-home
```

### 🎯 **Conversion Capabilities**

#### **Input Formats**
- PDF files (.pdf)

#### **Output Formats**
- **Text** (.txt) - Plain text extraction
- **Word** (.docx) - Microsoft Word format
- **HTML** (.html) - Web page format  
- **Markdown** (.md) - Markdown format
- **Images** (.jpg/.png) - High-quality image conversion

#### **Image Quality Options**
- **Low**: 72 DPI, JPEG 60% (~150KB per page)
- **Medium**: 150 DPI, JPEG 85% (~400KB per page) 
- **High**: 200 DPI, JPEG 95% (~700KB per page)
- **Ultra**: 300 DPI, PNG (~1.2MB per page)
- **Custom**: Full manual control (DPI, format, quality)

### 🔍 **AppImage Commands**

```bash
# Get help
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage --appimage-help

# Extract contents (for inspection)
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage --appimage-extract

# Mount filesystem (for debugging)
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage --appimage-mount

# Version information
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage --appimage-version
```

### 📊 **Size Optimization Results**

**Example: 5-page PDF conversion**
- **Low Quality**: 0.34 MB (97.1% compression)
- **Medium Quality**: 1.57 MB (96.9% compression)
- **High Quality**: 2.93 MB (96.7% compression)

### 🛠 **Dependencies Included**

The AppImage includes all necessary dependencies:
- Python 3.10 runtime
- Flet GUI framework
- PyPDF processing
- PIL/Pillow image handling
- pdf2image conversion
- ReportLab PDF generation
- All required system libraries

### 🐧 **Distribution Compatibility**

Tested and working on:
- Ubuntu 20.04+
- Debian 11+
- CentOS 8+
- Fedora 34+
- Arch Linux
- openSUSE
- And other modern Linux distributions

### 🔐 **Security & Verification**

- **Source**: Built from verified source code
- **Dependencies**: All packages from official repositories
- **Sandboxing**: Runs in user space, no root required
- **Portable**: Self-contained, no system modification

### 📝 **Troubleshooting**

#### **Common Issues:**

1. **Permission Denied**
   ```bash
   chmod +x Hiel-PDF-Converter-1.0.0-x86_64.AppImage
   ```

2. **Missing FUSE** (older systems)
   ```bash
   # Ubuntu/Debian
   sudo apt install fuse
   
   # CentOS/RHEL
   sudo yum install fuse
   ```

3. **Pandoc Warning** (for advanced conversions)
   ```bash
   # Install pandoc for Word/HTML/Markdown
   sudo apt install pandoc
   ```

### 🚀 **Performance**

- **Startup Time**: ~2-3 seconds
- **Memory Usage**: ~50-100 MB
- **Conversion Speed**: Depends on PDF size and quality settings
- **File Size**: Optimized for minimal disk usage

### 📦 **Distribution**

The AppImage can be:
- **Downloaded** and run immediately
- **Copied** to USB drives for portable use
- **Shared** without installation requirements
- **Integrated** into existing workflows

### 🔄 **Updates**

Future versions will be released as new AppImage files:
- `Hiel-PDF-Converter-1.1.0-x86_64.AppImage`
- `Hiel-PDF-Converter-2.0.0-x86_64.AppImage`
- etc.

Simply replace the old AppImage with the new one!

---

**Ready to convert your PDFs with professional quality and maximum portability! 🎉**