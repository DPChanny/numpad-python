#!/bin/bash
# Build script for Linux/macOS

echo "NumPad - Unix Build Script"
echo "=========================="

# Change to project root directory
cd "$(dirname "$0")/.."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not found in PATH"
    echo "Please install Anaconda or Miniconda"
    exit 1
fi

# Check if environment exists
if conda info --envs | grep -q "numpad"; then
    echo "Conda environment 'numpad' already exists."
else
    echo "Creating conda environment..."
    conda env create -f environment.yml
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create conda environment"
        exit 1
    fi
    echo "Environment created successfully!"
fi

# Activate environment and build
echo "Activating environment and building..."

# Source conda.sh to make conda activate work in script
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate numpad

if [ $? -ne 0 ]; then
    echo "Error: Failed to activate conda environment"
    exit 1
fi

# Install pyinstaller if not already installed
echo "Installing/updating pyinstaller..."
pip install pyinstaller

# Run the build script
echo "Running build script..."
python scripts/build.py

if [ $? -eq 0 ]; then
    echo ""
    echo "Build completed successfully!"
    echo "The executable can be found in the 'builds' directory."
    echo ""
else
    echo ""
    echo "Build failed. Please check the error messages above."
    echo ""
    exit 1
fi

# Deactivate environment
conda deactivate

echo "Build process completed!"

conda deactivate
