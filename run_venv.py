#!/usr/bin/env python3
"""
Company Risk Analysis System - Virtual Environment Launcher
Automatically activates the virtual environment and runs the application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_venv_exists():
    """Check if virtual environment exists"""
    venv_path = Path("company_risk_env")
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please run the setup script first:")
        print("  python setup_venv.py")
        return False
    return True

def get_python_executable():
    """Get the Python executable path from virtual environment"""
    if platform.system() == "Windows":
        return "company_risk_env\\Scripts\\python.exe"
    else:
        return "company_risk_env/bin/python"

def run_app():
    """Run the Flask application"""
    if not check_venv_exists():
        return False
    
    python_exe = get_python_executable()
    
    if not Path(python_exe).exists():
        print(f"❌ Python executable not found at: {python_exe}")
        print("Virtual environment may be corrupted. Please recreate it:")
        print("  python setup_venv.py")
        return False
    
    print("🚀 Starting Company Risk Analysis System from Virtual Environment...")
    print(f"📱 Application will be available at: http://localhost:5001")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the Flask app using the virtual environment Python
        subprocess.run([python_exe, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🔧 Company Risk Analysis System - Virtual Environment Launcher")
    print("=" * 60)
    
    if run_app():
        print("✅ Application completed successfully")
    else:
        print("❌ Failed to run application")
        sys.exit(1)

if __name__ == "__main__":
    main()
