#!/usr/bin/env python3
"""
Company Risk Analysis System - Virtual Environment Setup Script
Cross-platform Python script for setting up the virtual environment
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

def run_command(command, shell=False, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=shell, check=check, 
                              capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return e

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("Please install Python 3.8+ and try again")
        return False
    
    print(f"✅ Found Python {version.major}.{version.minor}.{version.micro}")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = Path("company_risk_env")
    
    if venv_path.exists():
        print("📦 Virtual environment already exists")
        return True
    
    print("📦 Creating virtual environment...")
    try:
        venv.create("company_risk_env", with_pip=True)
        print("✅ Virtual environment created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_activate_script():
    """Get the appropriate activation script path"""
    if platform.system() == "Windows":
        return "company_risk_env\\Scripts\\activate.bat"
    else:
        return "company_risk_env/bin/activate"

def install_dependencies():
    """Install Python dependencies"""
    print("📚 Installing Python dependencies...")
    
    # Determine the pip command based on platform
    if platform.system() == "Windows":
        pip_cmd = ["company_risk_env\\Scripts\\python.exe", "-m", "pip"]
    else:
        pip_cmd = ["company_risk_env/bin/pip"]
    
    # Upgrade pip first
    print("⬆️  Upgrading pip...")
    upgrade_result = run_command(pip_cmd + ["install", "--upgrade", "pip"], check=False)
    if upgrade_result.returncode != 0:
        print("⚠️  Warning: Failed to upgrade pip, continuing...")
    
    # Install requirements
    install_result = run_command(pip_cmd + ["install", "-r", "requirements.txt"])
    if install_result.returncode != 0:
        print("❌ Failed to install dependencies")
        return False
    
    print("✅ Dependencies installed successfully")
    return True

def create_directories():
    """Create necessary directories"""
    print("📁 Creating necessary directories...")
    
    directories = ["uploads"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  ✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 Setting up Company Risk Analysis System Virtual Environment")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    print("\n🎉 Virtual environment setup complete!")
    print("=" * 60)
    print("\nTo start using the system:")
    
    if platform.system() == "Windows":
        print("1. Activate the virtual environment: company_risk_env\\Scripts\\activate.bat")
    else:
        print("1. Activate the virtual environment: source company_risk_env/bin/activate")
    
    print("2. Run the application: python app.py")
    print("3. Open your browser to: http://localhost:5001")
    print("\nTo deactivate the virtual environment: deactivate")
    print("\nHappy analyzing! 🚀")
    
    # Show platform-specific instructions
    print(f"\n📋 Platform: {platform.system()} {platform.release()}")
    if platform.system() == "Windows":
        print("💡 Tip: You can also run 'setup_venv.bat' for Windows-specific setup")
    else:
        print("💡 Tip: You can also run 'setup_venv.sh' for Unix/Linux/macOS setup")

if __name__ == "__main__":
    main()
