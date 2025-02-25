import cv2
import os
import face_recognition
import csv
from datetime import datetime
import sqlite3
import numpy as np



#If program not working properly try adjusting tolerence value
TOLERENCE = 0.4 


# Database connection
conn = sqlite3.connect('attendance.db')
c = conn.cursor()


# Functions
def capture_photo(filename):
    """Captures a photo, detects faces, draws a white rectangle around them, and saves it with the given filename (temporarly)."""
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Capture Photo")
    
    frame_skip = 5  # Process every 5th frame for face detection to improve performance
    frame_count = 0
    face_locations = []

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        flipped_frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror effect
        
        # Only run face detection every 'frame_skip' frames
        if frame_count % frame_skip == 0:
            # Downscale the frame for faster face recognition
            small_frame = cv2.resize(flipped_frame, (0, 0), fx=0.5, fy=0.5)  
            face_locations = face_recognition.face_locations(small_frame)

            # Scale the face locations back to the original frame size
            face_locations = [(int(top * 2), int(right * 2), int(bottom * 2), int(left * 2)) 
                              for (top, right, bottom, left) in face_locations]

        # Draw white rectangles around the faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(flipped_frame, (left, top), (right, bottom), (255, 255, 255), 2)

        # Display the frame with rectangles around faces
        cv2.imshow("Capture Photo", flipped_frame)

        frame_count += 1
        key = cv2.waitKey(1)
        if key % 256 == 32:  # Space bar to capture
            cv2.imwrite(filename, cv2.flip(frame, 1))
            break

    cam.release()
    cv2.destroyAllWindows()

def register_student(roll_no, name):
    """Registers a new student."""
    if not roll_no or not name:
        return "Roll number and name are required!", False
    
    try:
        roll_no = int(roll_no)
    except ValueError:
        return "Roll no should be Integer", False

    # Check if the roll number already exists in the student database
    c.execute("SELECT name FROM student WHERE roll_no = ?", (roll_no,))
    result = c.fetchone()

    if result:
        return f"Student with roll number {roll_no} already registered as {result[0]}!", False

    photo_path = f"{roll_no}_{name}.jpg"
    capture_photo(photo_path)
    image = face_recognition.load_image_file(photo_path)
    os.remove(photo_path)

    face_locations = face_recognition.face_locations(image)
    no_of_Faces = len(face_locations)

    if no_of_Faces != 1:
        return f"There should be one face, {no_of_Faces} detected", False

    face_encoding = face_recognition.face_encodings(image)[0]
    face_encoding_blob = np.array(face_encoding).tobytes()

    try:
        c.execute("INSERT INTO student (roll_no, name, face_encoding) VALUES (?, ?, ?)", 
                  (roll_no, name, face_encoding_blob))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Roll number already exists!", False
    
    return f"Student {name} registered successfully!", True

def mark_attendance(roll_no):
    """Marks attendance by verifying the student."""
    if not roll_no:
        return "Roll number is required!", False
    
    try:
        roll_no = int(roll_no)
    except ValueError:
        return "Roll no should be Integer", False

    # Check if the roll number exists in the student database
    c.execute("SELECT name, face_encoding FROM student WHERE roll_no = ?", (roll_no,))
    result = c.fetchone()

    if not result:
        return "Roll number not registered!", False

    name, face_encoding_blob = result

    # Capture the current photo
    temp_photo = "temp_photo.jpg"
    capture_photo(temp_photo)

    temp_image = face_recognition.load_image_file(temp_photo)
    temp_encodings = face_recognition.face_encodings(temp_image)

    if not temp_encodings:
        os.remove(temp_photo)
        return "No face detected!", False

    saved_encoding = np.frombuffer(face_encoding_blob, dtype=np.float64)

    matches = face_recognition.compare_faces(temp_encodings, saved_encoding,  tolerance=TOLERENCE)
    if True in matches:
        log_attendance(roll_no, name)
        os.remove(temp_photo)
        return "Attendance marked successfully!", True

    os.remove(temp_photo)
    return "Face not recognized or matched!", False

def log_attendance(roll_no, name):
    """Logs attendance to the database."""
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("INSERT INTO attendance (roll_no, date_time) VALUES (?, ?)", (roll_no, date_time))
    conn.commit()

def get_attendance_data():
    """Fetches attendance data from the database."""
    c.execute("SELECT student.roll_no, student.name, attendance.date_time FROM attendance JOIN student ON attendance.roll_no = student.roll_no")
    rows = c.fetchall()
    data = []
    for row in rows:
        roll_no, name, date_time = row
        date, time = date_time.split(" ")
        data.append([roll_no, name, date, time])
    return data


def export_attendance(destination_path):
    """Exports the attendance data from the database to a CSV file at the desired location and clears the attendance table."""
    data = get_attendance_data()
    
    try:
        with open(destination_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Roll No", "Name", "Date", "Time"])  # Adding header
            writer.writerows(data)
        
        # Clear the attendance table after exporting
        c.execute("DELETE FROM attendance")
        conn.commit()
        
        return f"Attendance data exported to {destination_path}", True
    except Exception as e:
        return f"An error occurred while exporting the data: {e}", False

# Ensure the database connection is closed properly
import atexit
atexit.register(lambda: conn.close())