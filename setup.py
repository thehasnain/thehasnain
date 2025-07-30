#!/usr/bin/env python3
"""
Setup script for Face Recognition Attendance System
This script helps with initial setup and dependency checking
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"📱 Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_system_dependencies():
    """Check system-specific dependencies"""
    system = platform.system().lower()
    print(f"🖥️  Operating System: {system}")
    
    if system == "linux":
        print("📦 For Linux systems, you may need to install:")
        print("   sudo apt-get install build-essential cmake")
        print("   sudo apt-get install libopenblas-dev liblapack-dev")
        print("   sudo apt-get install libx11-dev libgtk-3-dev")
    elif system == "darwin":
        print("🍎 For macOS, you may need to install:")
        print("   brew install cmake")
        print("   brew install dlib")
    elif system == "windows":
        print("🪟 For Windows, you may need:")
        print("   Visual Studio Build Tools")
        print("   Or use conda: conda install -c conda-forge dlib")

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/faces',
        'static/css',
        'static/js',
        'templates',
        'exports'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def check_credentials():
    """Check if Google Sheets credentials exist"""
    if os.path.exists('credentials.json'):
        print("✅ Google Sheets credentials found")
    else:
        print("⚠️  Google Sheets credentials not found")
        print("📝 Please follow these steps:")
        print("   1. Go to Google Cloud Console")
        print("   2. Create a service account")
        print("   3. Download credentials.json")
        print("   4. Place it in the project root")

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing Python dependencies...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
        else:
            print("❌ Error installing dependencies:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {str(e)}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🔧 Face Recognition Attendance System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check system dependencies
    check_system_dependencies()
    print()
    
    # Create directories
    print("📁 Setting up directories...")
    create_directories()
    print()
    
    # Install dependencies
    if '--install-deps' in sys.argv:
        if not install_dependencies():
            sys.exit(1)
    print()
    
    # Check credentials
    check_credentials()
    print()
    
    print("🎉 Setup completed!")
    print("📚 Next steps:")
    print("   1. Set up Google Sheets API credentials")
    print("   2. Add student photos to static/faces/")
    print("   3. Run: python app.py")
    print("   4. Open http://localhost:5000")

if __name__ == '__main__':
    main()