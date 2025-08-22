# 🐍 Virtual Environment Guide for Company Risk Analysis System

This guide explains how to set up and use a Python virtual environment for the Company Risk Analysis System.

## 🎯 Why Use a Virtual Environment?

- **Isolation**: Keeps project dependencies separate from system Python
- **Version Control**: Prevents conflicts between different project requirements
- **Clean Environment**: Ensures consistent behavior across different machines
- **Easy Cleanup**: Simple to remove and recreate if needed

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

#### On macOS/Linux:
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

#### On Windows:
```cmd
setup_venv.bat
```

#### Cross-platform (Python):
```bash
python3 setup_venv.py
```

### Option 2: Manual Setup

#### 1. Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv company_risk_env

# Windows
python -m venv company_risk_env
```

#### 2. Activate Virtual Environment
```bash
# macOS/Linux
source company_risk_env/bin/activate

# Windows
company_risk_env\Scripts\activate.bat
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Create Uploads Directory
```bash
mkdir -p uploads
```

## 🔧 Using the Virtual Environment

### Starting the Application

#### Method 1: Use the Virtual Environment Launcher
```bash
python run_venv.py
```

#### Method 2: Manual Activation and Run
```bash
# Activate virtual environment
source company_risk_env/bin/activate  # macOS/Linux
# OR
company_risk_env\Scripts\activate.bat  # Windows

# Run the application
python app.py

# Deactivate when done
deactivate
```

#### Method 3: Direct Execution (Unix/Linux/macOS)
```bash
company_risk_env/bin/python app.py
```

### Verifying Virtual Environment

When the virtual environment is active, you should see `(company_risk_env)` at the beginning of your command prompt:

```bash
(company_risk_env) user@machine:~/company-risk-analysis$
```

## 📁 Virtual Environment Structure

After setup, your project will have this structure:

```
company-risk-analysis/
├── company_risk_env/        # Virtual environment directory
│   ├── bin/                # Unix/Linux/macOS executables
│   │   ├── python          # Python interpreter
│   │   ├── pip             # Package installer
│   │   └── activate        # Activation script
│   ├── Scripts/            # Windows executables
│   │   ├── python.exe      # Python interpreter
│   │   ├── pip.exe         # Package installer
│   │   └── activate.bat    # Activation script
│   ├── lib/                # Installed packages
│   └── pyvenv.cfg          # Virtual environment config
├── app.py                   # Main application
├── requirements.txt         # Dependencies
├── setup_venv.py           # Setup script
├── run_venv.py             # Virtual environment launcher
└── ...                     # Other project files
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Virtual Environment Not Found
```bash
❌ Virtual environment not found!
Please run the setup script first:
  python setup_venv.py
```

**Solution**: Run the setup script to create the virtual environment.

#### 2. Permission Denied (macOS/Linux)
```bash
❌ Permission denied: ./setup_venv.sh
```

**Solution**: Make the script executable:
```bash
chmod +x setup_venv.sh
```

#### 3. Python Not Found
```bash
❌ Python is not installed or not in PATH
```

**Solution**: Install Python 3.8+ and ensure it's in your PATH.

#### 4. Dependencies Installation Failed
```bash
❌ Failed to install dependencies
```

**Solution**: Check your internet connection and try again. Some packages may require system-level dependencies.

#### 5. Port Already in Use
```bash
Address already in use
Port 5001 is in use by another program
```

**Solution**: 
- Stop other applications using port 5001
- Change the port in `app.py`
- Kill existing processes: `lsof -ti:5001 | xargs kill -9`

### Recreating the Virtual Environment

If you encounter persistent issues, you can recreate the virtual environment:

```bash
# Remove existing virtual environment
rm -rf company_risk_env  # macOS/Linux
# OR
rmdir /s company_risk_env  # Windows

# Run setup again
python setup_venv.py
```

## 📋 Platform-Specific Instructions

### macOS

```bash
# Install Python (if not already installed)
brew install python3

# Setup virtual environment
python3 setup_venv.py

# Activate and run
source company_risk_env/bin/activate
python app.py
```

### Linux (Ubuntu/Debian)

```bash
# Install Python and venv
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Setup virtual environment
python3 setup_venv.py

# Activate and run
source company_risk_env/bin/activate
python app.py
```

### Windows

```cmd
# Install Python from python.org (if not already installed)

# Setup virtual environment
setup_venv.bat

# Activate and run
company_risk_env\Scripts\activate.bat
python app.py
```

## 🔄 Daily Usage Workflow

### Starting Your Work Session

1. **Navigate to project directory**:
   ```bash
   cd company-risk-analysis
   ```

2. **Activate virtual environment**:
   ```bash
   # macOS/Linux
   source company_risk_env/bin/activate
   
   # Windows
   company_risk_env\Scripts\activate.bat
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** to http://localhost:5001

### Ending Your Work Session

1. **Stop the application**: Press `Ctrl+C` in the terminal
2. **Deactivate virtual environment**:
   ```bash
   deactivate
   ```

## 🧹 Maintenance

### Updating Dependencies

```bash
# Activate virtual environment
source company_risk_env/bin/activate

# Update pip
pip install --upgrade pip

# Update specific packages
pip install --upgrade package_name

# Update all packages (use with caution)
pip list --outdated | cut -d ' ' -f1 | xargs -n1 pip install -U
```

### Checking Installed Packages

```bash
# Activate virtual environment
source company_risk_env/bin/activate

# List all packages
pip list

# Check outdated packages
pip list --outdated
```

### Exporting Dependencies

```bash
# Activate virtual environment
source company_risk_env/bin/activate

# Export current requirements
pip freeze > requirements_current.txt
```

## 🚀 Production Deployment

For production deployment, consider using:

- **Gunicorn** (WSGI server)
- **uWSGI** (WSGI server)
- **Docker** (containerization)
- **Virtual environment** on production server

### Example with Gunicorn

```bash
# Install gunicorn in virtual environment
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## 📚 Additional Resources

- [Python Virtual Environments Documentation](https://docs.python.org/3/tutorial/venv.html)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Pip User Guide](https://pip.pypa.io/en/stable/user_guide/)

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Verify Python version**: `python --version`
3. **Check virtual environment activation**: Look for `(venv)` in prompt
4. **Review error messages** carefully
5. **Check system requirements** and dependencies

---

**🎉 Happy coding with your virtual environment!**
