#!/bin/bash

# Hiel PDF Converter - Installation Script
# This script installs the Hiel PDF Converter application system-wide

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Hiel PDF Converter Installer  ${NC}"
    echo -e "${BLUE}         Version 1.0.0          ${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Check if running as root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        print_error "Please do not run this script as root"
        print_error "The script will request sudo permissions when needed"
        exit 1
    fi
}

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        print_error "Please install Python 3: sudo apt-get install python3"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(echo "$PYTHON_VERSION < 3.8" | bc -l) -eq 1 ]]; then
        print_error "Python 3.8 or higher is required (found $PYTHON_VERSION)"
        exit 1
    fi
    
    print_status "Python $PYTHON_VERSION found"
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required but not installed"
        print_error "Please install pip3: sudo apt-get install python3-pip"
        exit 1
    fi
    
    # Check venv
    if ! python3 -m venv --help &> /dev/null; then
        print_error "python3-venv is required but not installed"
        print_error "Please install python3-venv: sudo apt-get install python3-venv"
        exit 1
    fi
    
    print_status "All Python requirements satisfied"
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    # List of required packages
    PACKAGES=(
        "python3-dev"
        "python3-pip"
        "python3-venv"
        "pandoc"
        "poppler-utils"
        "libgtk-3-0"
        "libgstreamer1.0-0"
        "libgstreamer-plugins-base1.0-0"
    )
    
    # Check which packages are missing
    MISSING_PACKAGES=()
    for package in "${PACKAGES[@]}"; do
        if ! dpkg -l | grep -q "^ii  $package"; then
            MISSING_PACKAGES+=("$package")
        fi
    done
    
    if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
        print_warning "Missing packages: ${MISSING_PACKAGES[*]}"
        print_status "Installing missing packages..."
        
        sudo apt-get update
        sudo apt-get install -y "${MISSING_PACKAGES[@]}"
        
        if [ $? -ne 0 ]; then
            print_error "Failed to install system dependencies"
            exit 1
        fi
    else
        print_status "All system dependencies are already installed"
    fi
}

# Install application
install_application() {
    print_status "Installing Hiel PDF Converter..."
    
    # Get current directory
    SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Check if we're in the correct directory
    if [ ! -f "$SOURCE_DIR/main.py" ]; then
        print_error "main.py not found in $SOURCE_DIR"
        print_error "Please run this script from the application directory"
        exit 1
    fi
    
    # Create installation directory
    INSTALL_DIR="/opt/hiel-converter"
    print_status "Creating installation directory: $INSTALL_DIR"
    sudo mkdir -p "$INSTALL_DIR"
    
    # Copy application files
    print_status "Copying application files..."
    sudo cp -r "$SOURCE_DIR/domain" "$INSTALL_DIR/"
    sudo cp -r "$SOURCE_DIR/infrastructure" "$INSTALL_DIR/"
    sudo cp -r "$SOURCE_DIR/presentation" "$INSTALL_DIR/"
    sudo cp -r "$SOURCE_DIR/use_cases" "$INSTALL_DIR/"
    sudo cp -r "$SOURCE_DIR/config" "$INSTALL_DIR/"
    sudo cp -r "$SOURCE_DIR/assets" "$INSTALL_DIR/"
    sudo cp "$SOURCE_DIR/main.py" "$INSTALL_DIR/"
    sudo cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/"
    sudo cp "$SOURCE_DIR/README.md" "$INSTALL_DIR/"
    
    # Create virtual environment
    print_status "Creating virtual environment..."
    sudo python3 -m venv "$INSTALL_DIR/venv"
    
    # Install Python dependencies
    print_status "Installing Python dependencies..."
    sudo "$INSTALL_DIR/venv/bin/pip" install --upgrade pip
    sudo "$INSTALL_DIR/venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"
    
    # Set permissions
    print_status "Setting permissions..."
    sudo chown -R root:root "$INSTALL_DIR"
    sudo chmod -R 755 "$INSTALL_DIR"
    sudo chmod +x "$INSTALL_DIR/venv/bin/python"
    
    # Create launcher script
    print_status "Creating launcher script..."
    cat > "/tmp/hiel-converter-launcher.sh" << 'EOF'
#!/bin/bash
cd "/opt/hiel-converter"
source venv/bin/activate
python main.py "$@"
EOF
    
    sudo mv "/tmp/hiel-converter-launcher.sh" "/usr/local/bin/hiel-converter"
    sudo chmod +x "/usr/local/bin/hiel-converter"
    
    # Create desktop entry
    print_status "Creating desktop entry..."
    cat > "/tmp/hiel-converter.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Hiel PDF Converter
Comment=Convert PDF files to various formats
Exec=hiel-converter
Icon=/opt/hiel-converter/assets/hiel-converter.png
Terminal=false
Categories=Office;Graphics;Publishing;
StartupNotify=true
MimeType=application/pdf;
Keywords=PDF;converter;document;office;
GenericName=PDF Converter
EOF
    
    sudo mv "/tmp/hiel-converter.desktop" "/usr/share/applications/hiel-converter.desktop"
    sudo chmod 644 "/usr/share/applications/hiel-converter.desktop"
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        sudo update-desktop-database /usr/share/applications/
    fi
    
    print_status "Installation completed successfully!"
}

# Create uninstaller
create_uninstaller() {
    print_status "Creating uninstaller..."
    
    cat > "/tmp/hiel-converter-uninstall.sh" << 'EOF'
#!/bin/bash

# Hiel PDF Converter - Uninstaller

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_status "Uninstalling Hiel PDF Converter..."

# Remove application files
if [ -d "/opt/hiel-converter" ]; then
    print_status "Removing application files..."
    sudo rm -rf "/opt/hiel-converter"
fi

# Remove launcher
if [ -f "/usr/local/bin/hiel-converter" ]; then
    print_status "Removing launcher..."
    sudo rm "/usr/local/bin/hiel-converter"
fi

# Remove desktop entry
if [ -f "/usr/share/applications/hiel-converter.desktop" ]; then
    print_status "Removing desktop entry..."
    sudo rm "/usr/share/applications/hiel-converter.desktop"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    sudo update-desktop-database /usr/share/applications/
fi

# Remove user configuration (optional)
read -p "Remove user configuration files? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.hiel_converter"
    print_status "User configuration removed"
fi

print_status "Hiel PDF Converter has been uninstalled"
print_warning "This uninstaller will self-destruct in 3 seconds..."
sleep 3
rm -- "$0"
EOF
    
    sudo mv "/tmp/hiel-converter-uninstall.sh" "/usr/local/bin/hiel-converter-uninstall"
    sudo chmod +x "/usr/local/bin/hiel-converter-uninstall"
    
    print_status "Uninstaller created: /usr/local/bin/hiel-converter-uninstall"
}

# Main installation function
main() {
    print_header
    
    check_root
    check_requirements
    install_system_deps
    install_application
    create_uninstaller
    
    echo
    print_status "Installation completed successfully!"
    echo
    echo -e "${GREEN}To run the application:${NC}"
    echo -e "  ${YELLOW}From terminal: hiel-converter${NC}"
    echo -e "  ${YELLOW}From desktop: Look for 'Hiel PDF Converter' in applications menu${NC}"
    echo
    echo -e "${GREEN}To uninstall:${NC}"
    echo -e "  ${YELLOW}hiel-converter-uninstall${NC}"
    echo
    echo -e "${GREEN}Configuration files location:${NC}"
    echo -e "  ${YELLOW}~/.hiel_converter/${NC}"
    echo
}

# Run main function
main "$@"