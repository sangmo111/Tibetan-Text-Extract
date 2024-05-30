#!/bin/bash

# Install system-wide dependencies
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found, installing it first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    echo "Installing Tesseract..."
    brew install tesseract
    brew install tesseract-lang
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Updating package list..."
    sudo apt-get update
    echo "Installing Tesseract..."
    sudo apt-get install -y tesseract-ocr
    sudo apt-get install -y tesseract-ocr-bod  
fi

# Set up the virtual environment
echo "Creating virtual environment..."
python3 -m venv myenv
source myenv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete."