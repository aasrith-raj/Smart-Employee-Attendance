# 🧠 Face Recognition & Geolocation-Based Attendance System

A Python-based smart attendance system that uses face recognition and geolocation to mark employee attendance efficiently.

## 📌 Features

- 🎥 Real-time webcam-based face detection and recognition
- 🌍 Logs geolocation (latitude & longitude) using IP address
- 🗂️ Registers new employees with photo and ID
- 🧾 Logs attendance with timestamp, name, and location to a CSV file
- 🖥️ GUI interface using Tkinter for ease of use

## 🚀 How It Works

1. **Register New Employee**  
   - Use the GUI to capture a face and associate it with an ID and name.
   - Stored in the `dataset/` directory as `ID_Name.jpg`.

2. **Mark Attendance**  
   - Opens webcam and detects faces in real time.
   - Matches against registered employees using face encoding.
   - Logs attendance in `database.csv` with:
     - Timestamp
     - Employee name
     - Geolocation (IP-based)

3. **Employee List**  
   - Displays all registered employees from the dataset folder.

## 🧰 Technologies Used

- Python 3.11
- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [Pillow](https://python-pillow.org/)
- [Geocoder](https://geocoder.readthedocs.io/)

## 📁 Project Structure

