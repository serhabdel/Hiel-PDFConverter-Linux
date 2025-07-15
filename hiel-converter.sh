#!/bin/bash

# Hiel PDF Converter - Launch Script
# This script activates the virtual environment and launches the application

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$SCRIPT_DIR"

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
    echo -e "${BLUE}    Hiel PDF Converter v1.0     ${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Print header
print_header

# Check if we're in the correct directory
if [ ! -f "$APP_DIR/main.py" ]; then
    print_error "main.py not found in $APP_DIR"
    print_error "Please run this script from the application directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$APP_DIR/venv" ]; then
    print_error "Virtual environment not found"
    print_error "Please create a virtual environment first:"
    echo -e "  ${YELLOW}python3 -m venv venv${NC}"
    echo -e "  ${YELLOW}source venv/bin/activate${NC}"
    echo -e "  ${YELLOW}pip install -r requirements.txt${NC}"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "$APP_DIR/requirements.txt" ]; then
    print_error "requirements.txt not found"
    exit 1
fi

print_status "Activating virtual environment..."

# Activate virtual environment
source "$APP_DIR/venv/bin/activate"

# Check if activation was successful
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

print_status "Virtual environment activated"

# Check if Python is available
if ! command -v python &> /dev/null; then
    print_error "Python not found in virtual environment"
    exit 1
fi

# Check if required packages are installed
print_status "Checking dependencies..."

python -c "
import sys
missing_packages = []
required_packages = ['flet', 'pypdf', 'pdf2image', 'pillow', 'pypandoc', 'docx', 'reportlab']

for package in required_packages:
    try:
        if package == 'docx':
            import docx
        elif package == 'pillow':
            import PIL
        else:
            __import__(package)
    except ImportError:
        missing_packages.append(package)

if missing_packages:
    print(f'Missing packages: {missing_packages}')
    sys.exit(1)
else:
    print('All required packages are installed')
"

if [ $? -ne 0 ]; then
    print_error "Some required packages are missing"
    print_warning "Installing missing packages..."
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        print_error "Failed to install required packages"
        exit 1
    fi
fi

# Check if Pandoc is installed (required for some conversions)
if ! command -v pandoc &> /dev/null; then
    print_warning "Pandoc not found - Word/HTML/Markdown conversions may not work"
    print_warning "Install Pandoc with: sudo apt-get install pandoc"
fi

print_status "Starting Hiel PDF Converter..."

# Launch the application
python "$APP_DIR/main.py"

# Check exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    print_status "Application closed successfully"
else
    print_error "Application exited with error code $EXIT_CODE"
fi

# Deactivate virtual environment
deactivate

exit $EXIT_CODE