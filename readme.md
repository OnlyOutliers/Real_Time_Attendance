# 🎯 Face Recognition Attendance System

An automated attendance tracking system powered by facial recognition technology and Firebase real-time database.

## ✨ Features

- 📸 Real-time face detection and recognition
- ✅ Automated attendance marking
- 🔥 Firebase real-time database integration
- 👤 Student information display
- 🔄 Duplicate entry prevention (30s cooldown)
- ⚡ Multi-threaded performance

## 🚀 Getting Started

### Prerequisites

- Python 3.8
- Webcam
- Firebase Account

### Required Libraries

```bash
pip install opencv-python
pip install face-recognition
pip install numpy
pip install firebase-admin
pip install cvzone
```

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/OnlyOutliers/Real_Time_Attendance
   ```

2. **Firebase Configuration**
   - Create a Firebase project
   - Download `serviceaccountkey.json`
   - Place it in the project root
   - Update database URL in the code

3. **Initialize Database**
   ```bash
   python addDataToDataBase.py
   ```

4. **Generate Encodings**
   ```bash
   python encodegenerator.py
   ```

5. **Run the Application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
├── main.py                 # Main application
├── encodegenerator.py      # Face encoding generator
├── addDataToDataBase.py    # Database initializer
├── Images/
│   ├── Background/        # UI backgrounds
│   ├── Students/          # Student photos
│   └── state/            # UI state images
├── Encodefile.p           # Encoded faces
└── serviceaccountkey.json # Firebase credentials
```

## 💾 Database Structure

```json
{
    "Students": {
        "student_id": {
            "name": "Student Name",
            "major": "Department",
            "starting_year": "202X",
            "total_attendence": 0,
            "standing": "Grade",
            "Year": 1,
            "last_attendence_time": "YYYY-MM-DD HH:MM:SS"
        }
    }
}
```

## ⚙️ How It Works

1. Captures webcam feed
2. Detects and encodes faces
3. Matches with stored encodings
4. Updates attendance in Firebase
5. Displays student information
6. Prevents duplicate entries

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request


Project Link: [https://github.com/OnlyOutliers/Real_Time_Attendance](https://github.com/OnlyOutliers/Real_Time_Attendance)
