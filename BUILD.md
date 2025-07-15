# Hiel PDF Converter - Build & Distribution Guide

This guide explains how to build and distribute the Hiel PDF Converter application for Linux.

## Quick Start

### 1. Terminal Launch Script
```bash
# Run the application directly
./hiel-converter.sh
```

### 2. System Installation
```bash
# Install system-wide
sudo ./install.sh

# Run from anywhere
hiel-converter

# Uninstall
hiel-converter-uninstall
```

### 3. AppImage Build
```bash
# Build portable AppImage
cd build
./create-appimage.sh

# Run the AppImage
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage
```

## Detailed Instructions

### Terminal Launch Script (`hiel-converter.sh`)

**Purpose**: Direct execution from source directory
**Benefits**: 
- No installation required
- Automatic dependency checking
- Colored output with status messages
- Virtual environment activation

**Usage**:
```bash
./hiel-converter.sh
```

**Features**:
- ✅ Validates virtual environment
- ✅ Checks Python dependencies
- ✅ Warns about missing Pandoc
- ✅ Provides helpful error messages
- ✅ Automatic cleanup on exit

### System Installation (`install.sh`)

**Purpose**: Install application system-wide
**Benefits**:
- Desktop integration
- Application menu entry
- Command-line launcher
- Automatic dependency installation

**Installation Process**:
```bash
sudo ./install.sh
```

**What it does**:
1. Checks system requirements (Python 3.8+)
2. Installs system dependencies (pandoc, poppler-utils, etc.)
3. Creates `/opt/hiel-converter/` directory
4. Copies application files
5. Creates virtual environment with dependencies
6. Creates `/usr/local/bin/hiel-converter` launcher
7. Adds desktop entry to applications menu
8. Creates uninstaller script

**Files Created**:
- `/opt/hiel-converter/` - Application directory
- `/usr/local/bin/hiel-converter` - Command launcher
- `/usr/share/applications/hiel-converter.desktop` - Desktop entry
- `/usr/local/bin/hiel-converter-uninstall` - Uninstaller

### AppImage Build (`build/create-appimage.sh`)

**Purpose**: Create portable executable
**Benefits**:
- Single file distribution
- No installation required
- Runs on any Linux distribution
- Includes all dependencies

**Build Process**:
```bash
cd build
./create-appimage.sh
```

**Build Steps**:
1. Downloads `appimagetool` if not available
2. Creates AppDir structure
3. Copies Python runtime and libraries
4. Installs application dependencies
5. Copies system libraries
6. Creates desktop integration files
7. Builds final AppImage

**Output**: `Hiel-PDF-Converter-1.0.0-x86_64.AppImage`

## Distribution Options

### 1. Source Distribution
Distribute the entire project folder:
```bash
tar -czf hiel-converter-source.tar.gz "Hiel Converter Linux/"
```

Users run: `./hiel-converter.sh`

### 2. System Package
Use the installer script:
```bash
# Include in distribution
./install.sh
```

Users get desktop integration and command-line access.

### 3. AppImage (Recommended)
Single portable file:
```bash
# Build once
cd build && ./create-appimage.sh

# Distribute
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage
```

Perfect for users who want no installation.

## Build Requirements

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt-get install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    pandoc \
    poppler-utils \
    libgtk-3-0 \
    libgstreamer1.0-0 \
    libgstreamer-plugins-base1.0-0 \
    imagemagick \
    wget
```

### Python Dependencies
All handled automatically by the scripts, but listed in `requirements.txt`:
- flet==0.28.3
- pypdf==5.8.0
- pdf2image==1.17.0
- pypandoc==1.15
- python-docx==1.2.0
- Pillow==9.0.1
- reportlab==4.4.2

## File Structure

```
Hiel Converter Linux/
├── hiel-converter.sh          # Terminal launch script
├── install.sh                 # System installer
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # User documentation
├── BUILD.md                   # This file
├── assets/
│   ├── hiel-converter.png     # Application icon
│   └── hiel-converter.desktop # Desktop entry template
├── build/
│   ├── create-appimage.sh     # AppImage build script
│   └── AppDir/
│       ├── AppRun             # AppImage entry point
│       └── hiel-converter.desktop
├── domain/                    # Domain layer
├── infrastructure/            # Infrastructure layer
├── presentation/              # Presentation layer
├── use_cases/                 # Use cases layer
├── config/                    # Configuration layer
└── venv/                      # Virtual environment
```

## Testing Builds

### Test Terminal Script
```bash
./hiel-converter.sh
```

### Test Installation
```bash
# Install in test environment
sudo ./install.sh

# Test launcher
hiel-converter

# Test desktop entry
# Look for "Hiel PDF Converter" in applications menu

# Uninstall
hiel-converter-uninstall
```

### Test AppImage
```bash
cd build
./create-appimage.sh

# Test the AppImage
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage

# Test on different system
scp Hiel-PDF-Converter-1.0.0-x86_64.AppImage user@other-system:
ssh user@other-system
chmod +x Hiel-PDF-Converter-1.0.0-x86_64.AppImage
./Hiel-PDF-Converter-1.0.0-x86_64.AppImage
```

## Troubleshooting

### Common Issues

**Permission Denied**:
```bash
chmod +x hiel-converter.sh
chmod +x install.sh
chmod +x build/create-appimage.sh
```

**Missing Dependencies**:
```bash
# Install build dependencies
sudo apt-get install python3-dev python3-venv pandoc poppler-utils
```

**AppImage Build Fails**:
```bash
# Check appimagetool
which appimagetool

# Manual appimagetool install
cd build
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

**Virtual Environment Issues**:
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Distribution Checklist

- [ ] Test terminal script on clean system
- [ ] Test installation script
- [ ] Test AppImage on different distributions
- [ ] Verify all dependencies are included
- [ ] Test with sample PDF files
- [ ] Verify desktop integration works
- [ ] Test uninstaller
- [ ] Document system requirements
- [ ] Create release notes

## Release Process

1. **Tag Release**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **Build AppImage**:
   ```bash
   cd build
   ./create-appimage.sh
   ```

3. **Create Release Package**:
   ```bash
   tar -czf hiel-converter-v1.0.0.tar.gz "Hiel Converter Linux/"
   ```

4. **Upload to Release**:
   - Source: `hiel-converter-v1.0.0.tar.gz`
   - AppImage: `Hiel-PDF-Converter-1.0.0-x86_64.AppImage`

## Support

For build issues:
1. Check logs in `~/.hiel_converter/app.log`
2. Verify system requirements
3. Test with sample PDF files
4. Check GitHub issues