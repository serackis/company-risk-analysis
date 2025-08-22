@echo off
REM Company Risk Analysis System - Virtual Environment Setup Script (Windows)

echo 🚀 Setting up Company Risk Analysis System Virtual Environment
echo ================================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv company_risk_env

if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created successfully

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call company_risk_env\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    echo Please check requirements.txt and try again
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Create uploads directory
echo 📁 Creating uploads directory...
if not exist uploads mkdir uploads

echo.
echo 🎉 Virtual environment setup complete!
echo ================================================================
echo.
echo To start using the system:
echo 1. Activate the virtual environment: company_risk_env\Scripts\activate.bat
echo 2. Run the application: python app.py
echo 3. Open your browser to: http://localhost:5001
echo.
echo To deactivate the virtual environment: deactivate
echo.
echo Happy analyzing! 🚀
pause
