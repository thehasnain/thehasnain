# Face Recognition Attendance Web App

A comprehensive Python-based web application that uses facial recognition technology to automatically mark student attendance and store records in Google Sheets. The system includes an admin dashboard with data visualization, Excel export capabilities, and an AI-powered chatbot assistant.

## 🎯 Project Overview

This application was developed as part of a technical evaluation for Dr. C. V. Raman University Khandwa. It demonstrates the integration of computer vision, web development, cloud storage, and AI technologies in a practical attendance management system.

## ✨ Features

### Core Features
- **Real-time Face Recognition**: Uses OpenCV and face_recognition library for accurate face detection and recognition
- **Webcam Integration**: Browser-based camera access for seamless face capture
- **Google Sheets Integration**: Automatic attendance storage with duplicate prevention
- **Admin Dashboard**: Beautiful Bootstrap-powered interface for data management
- **Excel Export**: Multiple export options (daily, date range, monthly, all records)
- **Student Management**: Easy upload and management of student photos

### Bonus Features
- **AI Chatbot Assistant**: Rule-based chatbot for attendance queries and assistance
- **Data Visualization**: Statistics and attendance analytics
- **Search & Filter**: Advanced filtering options for attendance records
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Live attendance tracking and notifications

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Computer Vision**: OpenCV, face_recognition, dlib
- **Database**: Google Sheets API
- **Data Processing**: Pandas, NumPy
- **Excel Export**: openpyxl, xlsxwriter
- **UI Components**: Font Awesome, DataTables
- **Authentication**: Google Service Account

## 📋 Prerequisites

Before setting up the project, ensure you have:

1. **Python 3.8 or higher** installed
2. **Git** for cloning the repository
3. **Google Cloud Account** for Sheets API access
4. **Webcam/Camera** for face recognition
5. **Modern web browser** with camera support

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/face-recognition-attendance.git
cd face-recognition-attendance
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Google Sheets API Setup

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API and Google Drive API

2. **Create Service Account**:
   - Go to IAM & Admin → Service Accounts
   - Click "Create Service Account"
   - Fill in details and create
   - Generate JSON key file

3. **Configure Credentials**:
   - Download the JSON credentials file
   - Rename it to `credentials.json`
   - Place it in the project root directory

4. **Create Google Sheet**:
   - Create a new Google Sheet named "Attendance_Sheet"
   - Share it with your service account email (found in credentials.json)
   - Give edit permissions

### Step 5: Environment Configuration

Copy the `.env` file and update values:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Step 6: Add Student Photos

1. Create student photo files in `static/faces/` directory
2. Name files as `StudentName.jpg` (e.g., `John_Doe.jpg`, `Alice_Smith.jpg`)
3. Ensure photos are clear, front-facing, and well-lit
4. Supported formats: JPG, JPEG, PNG

### Step 7: Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
face-recognition-attendance/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── credentials.json           # Google Sheets API credentials
├── .env                       # Environment configuration
├── README.md                  # Project documentation
│
├── templates/
│   ├── index.html            # Webcam capture page
│   └── dashboard.html        # Admin dashboard
│
├── static/
│   ├── faces/               # Student photos directory
│   ├── css/                 # Custom stylesheets
│   └── js/                  # Custom JavaScript
│
└── exports/                 # Excel export files
```

## 🎮 Usage Guide

### For Students (Attendance Marking)

1. **Access Main Page**: Navigate to `http://localhost:5000`
2. **Start Camera**: Click "Start Camera" button
3. **Position Face**: Ensure your face is visible and well-lit
4. **Capture**: Click "Capture & Recognize" button
5. **Confirmation**: System will show recognition results and attendance status

### For Administrators (Dashboard)

1. **Access Dashboard**: Navigate to `http://localhost:5000/dashboard`
2. **View Statistics**: Check attendance statistics at the top
3. **Manage Students**: Add new students by uploading their photos
4. **Filter Data**: Use date range and name filters
5. **Export Reports**: Choose from various export options
6. **AI Assistant**: Click the chatbot icon for assistance

### AI Chatbot Commands

The AI assistant can help with:
- `"How many students attended today?"`
- `"Show attendance for John in July"`
- `"Download this month's report"`
- `"Export attendance data"`

## 📊 Google Sheets Structure

The system creates a sheet with the following columns:
- **Name**: Student name
- **Date**: Attendance date (YYYY-MM-DD)
- **Time**: Attendance time (HH:MM:SS)
- **Status**: Attendance status (Present)

## 🔧 Configuration Options

### Environment Variables (.env)

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
GOOGLE_SHEETS_CREDENTIALS=credentials.json
SPREADSHEET_NAME=Attendance_Sheet
```

### Face Recognition Settings

- **Tolerance**: Adjust in `app.py` (default: 0.6)
- **Image Quality**: Modify canvas quality in templates
- **Recognition Confidence**: Threshold for face matching

## 🚨 Troubleshooting

### Common Issues

1. **Camera Not Working**:
   - Check browser permissions
   - Ensure HTTPS (required for camera access)
   - Try different browsers

2. **Face Not Recognized**:
   - Ensure good lighting
   - Use clear, front-facing photos
   - Check photo naming convention

3. **Google Sheets Connection Failed**:
   - Verify credentials.json is correct
   - Check if sheet is shared with service account
   - Ensure APIs are enabled

4. **Import Errors**:
   - Check Python version (3.8+)
   - Reinstall dependencies: `pip install -r requirements.txt`
   - Install system dependencies for face_recognition

### System Dependencies

**For Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev
```

**For macOS**:
```bash
brew install cmake
brew install dlib
```

**For Windows**:
- Install Visual Studio Build Tools
- Use conda: `conda install -c conda-forge dlib`

## 🔐 Security Considerations

1. **Credentials Security**:
   - Never commit `credentials.json` to version control
   - Use environment variables for sensitive data
   - Rotate service account keys regularly

2. **Data Privacy**:
   - Implement proper access controls
   - Consider GDPR compliance for student data
   - Use HTTPS in production

3. **Face Data Protection**:
   - Store face encodings securely
   - Implement data retention policies
   - Consider encryption for sensitive photos

## 🚀 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

### Environment Setup

- Set `FLASK_ENV=production`
- Use a proper secret key
- Configure logging
- Set up SSL certificates
- Use a reverse proxy (nginx)

## 📈 Performance Optimization

1. **Face Recognition**:
   - Reduce image resolution for processing
   - Implement face detection caching
   - Use smaller face encoding models

2. **Database**:
   - Implement connection pooling
   - Cache frequently accessed data
   - Use database indexes

3. **Frontend**:
   - Minify CSS/JS files
   - Implement image compression
   - Use CDN for static assets

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial Development* - [GitHub Profile](https://github.com/your-username)

## 🙏 Acknowledgments

- Dr. C. V. Raman University Khandwa for the project opportunity
- OpenCV and face_recognition library contributors
- Flask and Bootstrap communities
- Google Sheets API documentation

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Email: your-email@example.com
- Documentation: [Project Wiki](https://github.com/your-username/face-recognition-attendance/wiki)

## 🎯 Future Enhancements

- [ ] OpenAI GPT integration for advanced chatbot
- [ ] Real-time notifications
- [ ] Mobile app development
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Biometric authentication
- [ ] Cloud deployment automation

---

**Built with ❤️ for educational and institutional use**
