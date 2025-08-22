#!/bin/bash

# Company Risk Analysis System - Virtual Environment Setup Script

echo "🚀 Setting up Company Risk Analysis System Virtual Environment"
echo "================================================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv company_risk_env

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created successfully"

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source company_risk_env/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "Please check requirements.txt and try again"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p uploads

echo ""
echo "🎉 Virtual environment setup complete!"
echo "================================================================"
echo ""
echo "To start using the system:"
echo "1. Activate the virtual environment: source company_risk_env/bin/activate"
echo "2. Run the application: python app.py"
echo "3. Open your browser to: http://localhost:5001"
echo ""
echo "To deactivate the virtual environment: deactivate"
echo ""
echo "Happy analyzing! 🚀"
