from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import base64
import io
from PIL import Image
import json
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.secret_key = 'demo-secret-key-for-testing'

# Global variables for face recognition
known_face_names = []
UPLOAD_FOLDER = 'static/faces'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Google Sheets configuration
GOOGLE_SHEETS_CREDENTIALS = 'credentials.json'
SPREADSHEET_NAME = 'Attendance_Sheet'

class AttendanceSystem:
    def __init__(self):
        self.sheet = None
        self.setup_google_sheets()
        self.load_known_faces()
    
    def setup_google_sheets(self):
        """Initialize Google Sheets connection (Demo mode)"""
        print("📊 Google Sheets: Running in demo mode")
        self.sheet = None
    
    def load_known_faces(self):
        """Load known faces from the faces directory"""
        global known_face_names
        
        known_face_names = []
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            return
        
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                name = os.path.splitext(filename)[0]
                known_face_names.append(name)
                print(f"📷 Loaded face for: {name}")
        
        print(f"✅ Loaded {len(known_face_names)} known faces")
    
    def recognize_face(self, image_data):
        """Simulate face recognition (Demo mode)"""
        try:
            # In demo mode, we'll simulate recognition
            if known_face_names:
                # Return first known face as demo
                return [{
                    'name': known_face_names[0],
                    'confidence': 0.85
                }]
            else:
                return []
        except Exception as e:
            print(f"Error in face recognition: {str(e)}")
            return []
    
    def mark_attendance(self, name):
        """Mark attendance (Demo mode - just log to console)"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            
            print(f"📝 Demo: Marking attendance for {name} on {today} at {current_time}")
            return True, f"Demo: Attendance marked successfully for {name}"
            
        except Exception as e:
            return False, f"Error marking attendance: {str(e)}"
    
    def get_attendance_data(self, start_date=None, end_date=None, name_filter=None):
        """Get demo attendance data"""
        # Return some demo data
        demo_data = [
            {"Name": "John Doe", "Date": "2024-01-15", "Time": "09:30:00", "Status": "Present"},
            {"Name": "Alice Smith", "Date": "2024-01-15", "Time": "09:45:00", "Status": "Present"},
            {"Name": "Bob Johnson", "Date": "2024-01-16", "Time": "09:15:00", "Status": "Present"},
        ]
        return demo_data
    
    def export_to_excel(self, start_date=None, end_date=None, export_type='all'):
        """Export demo data to Excel"""
        try:
            records = self.get_attendance_data()
            
            if not records:
                return None, "No data to export"
            
            df = pd.DataFrame(records)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"demo_attendance_{timestamp}.xlsx"
            filepath = os.path.join('exports', filename)
            os.makedirs('exports', exist_ok=True)
            
            df.to_excel(filepath, index=False, sheet_name='Attendance')
            return filepath, "Export successful"
            
        except Exception as e:
            return None, f"Export failed: {str(e)}"

# Initialize attendance system
attendance_system = AttendanceSystem()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with webcam capture"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    attendance_data = attendance_system.get_attendance_data()
    
    # Get summary statistics
    if attendance_data:
        df = pd.DataFrame(attendance_data)
        total_students = len(df['Name'].unique())
        total_attendance = len(df)
        today_attendance = len(df[df['Date'] == datetime.now().strftime('%Y-%m-%d')])
    else:
        total_students = total_attendance = today_attendance = 0
    
    stats = {
        'total_students': total_students,
        'total_attendance': total_attendance,
        'today_attendance': today_attendance
    }
    
    return render_template('dashboard.html', 
                         attendance_data=attendance_data,
                         stats=stats,
                         known_faces=known_face_names)

@app.route('/recognize', methods=['POST'])
def recognize():
    """Handle face recognition from webcam (Demo mode)"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data received'})
        
        # Demo recognition
        recognized_faces = attendance_system.recognize_face(image_data)
        
        if recognized_faces:
            best_match = recognized_faces[0]
            name = best_match['name']
            confidence = best_match['confidence']
            
            success, message = attendance_system.mark_attendance(name)
            
            return jsonify({
                'success': True,
                'name': name,
                'confidence': confidence,
                'attendance_marked': success,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Demo mode: Add student photos to test recognition'
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/upload_face', methods=['POST'])
def upload_face():
    """Upload new student face"""
    try:
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(url_for('dashboard'))
        
        file = request.files['file']
        name = request.form.get('student_name', '').strip()
        
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('dashboard'))
        
        if not name:
            flash('Student name is required')
            return redirect(url_for('dashboard'))
        
        if file and allowed_file(file.filename):
            filename = f"{secure_filename(name)}.jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            file.save(filepath)
            attendance_system.load_known_faces()
            
            flash(f'Face added successfully for {name}')
        else:
            flash('Invalid file type. Please upload JPG, JPEG, or PNG files.')
            
    except Exception as e:
        flash(f'Error uploading file: {str(e)}')
    
    return redirect(url_for('dashboard'))

@app.route('/api/attendance')
def api_attendance():
    """API endpoint for attendance data"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    name_filter = request.args.get('name')
    
    data = attendance_system.get_attendance_data(start_date, end_date, name_filter)
    return jsonify(data)

@app.route('/export')
def export_attendance():
    """Export attendance to Excel"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    export_type = request.args.get('type', 'all')
    
    filepath, message = attendance_system.export_to_excel(start_date, end_date, export_type)
    
    if filepath:
        return send_file(filepath, as_attachment=True, download_name=os.path.basename(filepath))
    else:
        flash(message)
        return redirect(url_for('dashboard'))

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """Simple chatbot for attendance queries"""
    try:
        data = request.get_json()
        query = data.get('query', '').lower()
        
        response = ""
        
        if 'how many' in query and 'attended' in query:
            if 'today' in query:
                response = "Demo mode: 3 students attended today."
            else:
                response = "Demo mode: Total attendance records: 15"
        
        elif 'attendance for' in query:
            response = "Demo mode: Student has 5 attendance records this month."
        
        elif 'download' in query or 'export' in query:
            response = "You can export attendance data using the Export buttons in the dashboard."
        
        else:
            response = "Demo mode: I can help with attendance queries. Try asking about today's attendance!"
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'})

@app.route('/status')
def status():
    """Status endpoint for debugging"""
    return jsonify({
        'status': 'running',
        'mode': 'demo',
        'known_faces': len(known_face_names),
        'faces': known_face_names,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("🚀 Starting Face Recognition Attendance System (Demo Mode)...")
    print(f"📊 Debug mode: True")
    print(f"🌐 Access the application at: http://localhost:5000")
    print(f"🔧 Admin dashboard at: http://localhost:5000/dashboard")
    print(f"📋 Status endpoint: http://localhost:5000/status")
    print("📱 Demo mode: Face recognition simulation enabled")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)