#!/usr/bin/env python3
"""
Quick Start Script for Face Recognition Attendance System

This script helps you get the application running quickly with minimal setup.
Perfect for testing and demonstration purposes.
"""

import os
import sys
import json
import shutil
from datetime import datetime

def create_demo_credentials():
    """Create demo credentials for testing without Google Sheets"""
    demo_creds = {
        "type": "service_account",
        "project_id": "demo-project",
        "private_key_id": "demo-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nDEMO_KEY\n-----END PRIVATE KEY-----\n",
        "client_email": "demo@demo-project.iam.gserviceaccount.com",
        "client_id": "demo-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/demo%40demo-project.iam.gserviceaccount.com"
    }
    
    with open('credentials.json', 'w') as f:
        json.dump(demo_creds, f, indent=2)
    
    print("📝 Created demo credentials.json")
    print("⚠️  Note: This is for testing only. Google Sheets won't work with demo credentials.")

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'templates/dashboard.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def setup_demo_environment():
    """Set up a demo environment for quick testing"""
    print("🚀 Setting up demo environment...")
    
    # Create directories
    directories = ['static/faces', 'exports', 'static/css', 'static/js']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Create demo credentials if not exists
    if not os.path.exists('credentials.json'):
        create_demo_credentials()
    
    # Create .env file if not exists
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("FLASK_APP=app.py\n")
            f.write("FLASK_ENV=development\n")
            f.write("SECRET_KEY=demo-secret-key-for-testing\n")
        print("📝 Created .env file")
    
    print("✅ Demo environment setup complete!")

def show_instructions():
    """Show quick start instructions"""
    print("\n" + "="*60)
    print("🎉 QUICK START INSTRUCTIONS")
    print("="*60)
    print()
    print("1. 📦 Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. 📸 Add student photos (optional for demo):")
    print("   - Add photos to static/faces/ directory")
    print("   - Name them as: StudentName.jpg")
    print("   - Example: John_Doe.jpg, Alice_Smith.jpg")
    print()
    print("3. 🚀 Run the application:")
    print("   python app.py")
    print("   or")
    print("   python run.py")
    print()
    print("4. 🌐 Open in browser:")
    print("   http://localhost:5000 (Main page)")
    print("   http://localhost:5000/dashboard (Admin dashboard)")
    print()
    print("📝 NOTES:")
    print("- Camera access requires HTTPS in production")
    print("- Demo credentials won't connect to Google Sheets")
    print("- For full functionality, set up real Google Sheets API")
    print()
    print("🆘 Need help? Check README.md for detailed instructions")
    print("="*60)

def main():
    """Main quick start function"""
    print("⚡ Face Recognition Attendance - Quick Start")
    print("-" * 50)
    
    # Check if we're in the right directory
    if not check_requirements():
        print("\n❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Setup demo environment
    setup_demo_environment()
    
    # Show instructions
    show_instructions()
    
    # Ask if user wants to start the app
    response = input("\n🚀 Start the application now? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        try:
            print("\n📡 Starting Flask application...")
            os.system("python app.py")
        except KeyboardInterrupt:
            print("\n👋 Application stopped. Thanks for trying the demo!")
    else:
        print("\n👋 Setup complete! Run 'python app.py' when ready.")

if __name__ == '__main__':
    main()