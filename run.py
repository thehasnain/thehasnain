#!/usr/bin/env python3
"""
Simple runner script for the Face Recognition Attendance Web App
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Check if running in development or production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 Starting Face Recognition Attendance System...")
    print(f"📊 Debug mode: {debug_mode}")
    print(f"🌐 Access the application at: http://localhost:5000")
    print(f"🔧 Admin dashboard at: http://localhost:5000/dashboard")
    print("📱 Make sure your camera is connected and working!")
    print("-" * 50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=debug_mode,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        sys.exit(1)