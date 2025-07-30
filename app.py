from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import cv2
import face_recognition
import numpy as np
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import os
import base64
import io
from PIL import Image
import json
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Global variables for face recognition
known_face_encodings = []
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
        """Initialize Google Sheets connection"""
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            if os.path.exists(GOOGLE_SHEETS_CREDENTIALS):
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    GOOGLE_SHEETS_CREDENTIALS, scope)
                client = gspread.authorize(creds)
                
                # Try to open existing sheet or create new one
                try:
                    spreadsheet = client.open(SPREADSHEET_NAME)
                    self.sheet = spreadsheet.sheet1
                except gspread.SpreadsheetNotFound:
                    # Create new spreadsheet
                    spreadsheet = client.create(SPREADSHEET_NAME)
                    self.sheet = spreadsheet.sheet1
                    # Set headers
                    self.sheet.append_row(['Name', 'Date', 'Time', 'Status'])
                
                print("Google Sheets connected successfully!")
            else:
                print("Google Sheets credentials not found. Please add credentials.json")
                
        except Exception as e:
            print(f"Error setting up Google Sheets: {str(e)}")
            self.sheet = None
    
    def load_known_faces(self):
        """Load and encode known faces from the faces directory"""
        global known_face_encodings, known_face_names
        
        known_face_encodings = []
        known_face_names = []
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
            return
        
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    # Load image file
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image = face_recognition.load_image_file(image_path)
                    
                    # Get face encodings
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        # Use the first face found in the image
                        face_encoding = face_encodings[0]
                        known_face_encodings.append(face_encoding)
                        
                        # Use filename (without extension) as name
                        name = os.path.splitext(filename)[0]
                        known_face_names.append(name)
                        
                        print(f"Loaded face for: {name}")
                    else:
                        print(f"No face found in {filename}")
                        
                except Exception as e:
                    print(f"Error loading {filename}: {str(e)}")
        
        print(f"Loaded {len(known_face_names)} known faces")
    
    def recognize_face(self, image_data):
        """Recognize face from base64 image data"""
        try:
            # Decode base64 image
            image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64,
            image_bytes = base64.b64decode(image_data)
            
            # Convert to PIL Image
            pil_image = Image.open(io.BytesIO(image_bytes))
            
            # Convert PIL image to numpy array (RGB)
            rgb_image = np.array(pil_image.convert('RGB'))
            
            # Find face locations and encodings
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            recognized_names = []
            
            for face_encoding in face_encodings:
                # Compare with known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        recognized_names.append({
                            'name': name,
                            'confidence': float(confidence)
                        })
            
            return recognized_names
            
        except Exception as e:
            print(f"Error in face recognition: {str(e)}")
            return []
    
    def mark_attendance(self, name):
        """Mark attendance for a student"""
        if not self.sheet:
            return False, "Google Sheets not connected"
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            
            # Check if already marked today
            existing_records = self.sheet.get_all_records()
            for record in existing_records:
                if record['Name'] == name and record['Date'] == today:
                    return False, f"Attendance already marked for {name} today"
            
            # Add new attendance record
            self.sheet.append_row([name, today, current_time, 'Present'])
            return True, f"Attendance marked successfully for {name}"
            
        except Exception as e:
            return False, f"Error marking attendance: {str(e)}"
    
    def get_attendance_data(self, start_date=None, end_date=None, name_filter=None):
        """Get attendance data with optional filters"""
        if not self.sheet:
            return []
        
        try:
            records = self.sheet.get_all_records()
            df = pd.DataFrame(records)
            
            if df.empty:
                return []
            
            # Apply filters
            if start_date:
                df = df[df['Date'] >= start_date]
            if end_date:
                df = df[df['Date'] <= end_date]
            if name_filter:
                df = df[df['Name'].str.contains(name_filter, case=False)]
            
            return df.to_dict('records')
            
        except Exception as e:
            print(f"Error getting attendance data: {str(e)}")
            return []
    
    def export_to_excel(self, start_date=None, end_date=None, export_type='all'):
        """Export attendance data to Excel"""
        try:
            records = self.get_attendance_data(start_date, end_date)
            
            if not records:
                return None, "No data to export"
            
            df = pd.DataFrame(records)
            
            # Create filename based on export type
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            if export_type == 'monthly':
                filename = f"attendance_monthly_{timestamp}.xlsx"
            elif start_date and end_date:
                filename = f"attendance_{start_date}_to_{end_date}_{timestamp}.xlsx"
            else:
                filename = f"attendance_all_{timestamp}.xlsx"
            
            filepath = os.path.join('exports', filename)
            os.makedirs('exports', exist_ok=True)
            
            # Export to Excel
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Attendance', index=False)
                
                # Add summary sheet
                summary_df = df.groupby('Name').agg({
                    'Date': 'count',
                    'Date': ['min', 'max']
                }).round(2)
                summary_df.columns = ['Total_Days', 'First_Attendance', 'Last_Attendance']
                summary_df.to_excel(writer, sheet_name='Summary')
            
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
    # Get recent attendance data
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
                         attendance_data=attendance_data[:50],  # Show recent 50 records
                         stats=stats,
                         known_faces=known_face_names)

@app.route('/recognize', methods=['POST'])
def recognize():
    """Handle face recognition from webcam"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data received'})
        
        # Recognize faces
        recognized_faces = attendance_system.recognize_face(image_data)
        
        if recognized_faces:
            # Take the best match
            best_match = max(recognized_faces, key=lambda x: x['confidence'])
            name = best_match['name']
            confidence = best_match['confidence']
            
            # Mark attendance
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
                'message': 'No known face recognized'
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
            # Create filename with student name
            filename = f"{secure_filename(name)}.jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            file.save(filepath)
            
            # Reload known faces
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
        
        # Simple rule-based responses
        response = ""
        
        if 'how many' in query and 'attended' in query:
            # Extract date if mentioned
            if 'today' in query:
                date = datetime.now().strftime('%Y-%m-%d')
                records = attendance_system.get_attendance_data(start_date=date, end_date=date)
                count = len(records)
                response = f"Today ({date}), {count} students attended."
            else:
                records = attendance_system.get_attendance_data()
                count = len(records)
                response = f"Total attendance records: {count}"
        
        elif 'attendance for' in query:
            # Extract name
            words = query.split()
            if 'for' in words:
                name_index = words.index('for') + 1
                if name_index < len(words):
                    name = words[name_index].capitalize()
                    records = attendance_system.get_attendance_data(name_filter=name)
                    count = len(records)
                    response = f"{name} has {count} attendance records."
        
        elif 'download' in query or 'export' in query:
            response = "You can export attendance data using the Export buttons in the dashboard. Choose from daily, date range, or monthly exports."
        
        else:
            response = "I can help you with attendance queries. Try asking: 'How many students attended today?' or 'Show attendance for [student name]'"
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'response': f'Sorry, I encountered an error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)