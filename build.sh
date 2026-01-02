#!/usr/bin/env bash

set -e  # Exit on error

# Ensure mise is available and install Python version from .tool-version
if command -v mise &> /dev/null; then
  echo "Installing Python version with mise..."
  mise plugins update 2>/dev/null || true
  mise install
  PYTHON_CMD=$(mise which python)
else
  echo "mise not found, using system python"
  PYTHON_CMD=python
fi

# Remove existing venv if it exists
if [ -d "venv" ]; then
  echo "Removing existing virtualenv..."
  rm -rf venv
fi

# Create new virtualenv
echo "Creating virtualenv..."
$PYTHON_CMD -m venv venv

# Activate virtualenv and install dependencies
echo "Installing dependencies..."
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Build complete! Virtualenv created at ./venv"
echo "To activate: source venv/bin/activate"
