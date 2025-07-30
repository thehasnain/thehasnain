from flask import Flask, render_template, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'debug-key'

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    # Demo data for testing
    demo_stats = {
        'total_students': 5,
        'total_attendance': 15,
        'today_attendance': 3
    }
    
    demo_attendance = [
        {"Name": "John Doe", "Date": "2024-01-15", "Time": "09:30:00", "Status": "Present"},
        {"Name": "Alice Smith", "Date": "2024-01-15", "Time": "09:45:00", "Status": "Present"}
    ]
    
    demo_faces = ["John_Doe", "Alice_Smith", "Bob_Johnson"]
    
    return render_template('dashboard.html', 
                         attendance_data=demo_attendance,
                         stats=demo_stats,
                         known_faces=demo_faces)

@app.route('/status')
def status():
    """Debug status endpoint"""
    return jsonify({
        'status': 'running',
        'mode': 'debug',
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'templates_folder': app.template_folder,
        'static_folder': app.static_folder,
        'templates_exist': {
            'index.html': os.path.exists('templates/index.html'),
            'dashboard.html': os.path.exists('templates/dashboard.html')
        }
    })

@app.route('/recognize', methods=['POST'])
def recognize():
    """Demo recognition endpoint"""
    return jsonify({
        'success': True,
        'name': 'Demo User',
        'confidence': 0.85,
        'attendance_marked': True,
        'message': 'Debug mode: Recognition simulated successfully'
    })

if __name__ == '__main__':
    print("🔧 DEBUG MODE - Face Recognition Attendance System")
    print(f"🌐 URL: http://localhost:5000")
    print(f"📋 Status: http://localhost:5000/status") 
    print(f"🎯 Dashboard: http://localhost:5000/dashboard")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)