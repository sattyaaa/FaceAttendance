# Facial Recognition Attendance System

This Python project is a **Facial Recognition Attendance System** that uses `OpenCV`, `face_recognition`, and `tkinter` for capturing photos, recognizing faces, and managing attendance. The application allows you to register students and mark attendance seamlessly through a user-friendly graphical interface.

---

## Features

1. **Register Students**:
   - Capture a photo of a student.
   - Ensure only one face is detected.
   - Save the photo with the student's Roll No and Name.

2. **Mark Attendance**:
   - Capture a live photo of the student.
   - Match the photo with the registered record.
   - Log attendance (Roll No, Name, Date, and Time) in a CSV file.

3. **View Attendance**:
   - Display all attendance records in a tabular format.
   - Refresh attendance records in real-time.

---

## Requirements

### Libraries
- `cv2` (OpenCV)
- `os`
- `face_recognition`
- `csv`
- `tkinter`
- `datetime`

### Installation
#### Install the required Python libraries using:
   ```bash
   pip install opencv-python face_recognition
   ```
   - If installation not working try manually installing dlib from [https://github.com/z-mahmud22/Dlib_Windows_Python3.x](https://github.com/z-mahmud22/Dlib_Windows_Python3.x)

   - You might also need to downgrade your numpy to ```numpy==1.26.4```


## Usage

 **Run the Program**:
   - Launch the application by running:
     ```bash
     python app.py
     ```

### Tolerence
If result is not accurate try changing `TOLERENCE` value in ```attendance.py```

## Author

Created by [sattyaaa](https://github.com/sattyaaa).
