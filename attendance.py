import cv2
import os
import face_recognition
import csv
from datetime import datetime

# Paths
PHOTO_FOLDER = "photos"
ATTENDANCE_FILE = "attendance.csv"
TOLERENCE = 0.4 #If program not working properly try adjusting tolerence value

# Ensure directories and files exist
os.makedirs(PHOTO_FOLDER, exist_ok=True)
if not os.path.exists(ATTENDANCE_FILE) or os.stat(ATTENDANCE_FILE).st_size == 0:
    with open(ATTENDANCE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Roll No", "Name", "Date", "Time"])

# Functions
def capture_photo(filename):
    """Captures a photo, detects faces, draws a white rectangle around them, and saves it with the given filename."""
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
            print(f"Photo saved as {filename}")
            break

    cam.release()
    cv2.destroyAllWindows()

def register_student(roll_no, name):
    """Registers a new student."""
    if not roll_no or not name:
        return "Roll number and name are required!" , False
    
    try:
        roll_no=int(roll_no)
    except ValueError:
        return "Roll no should be Integer", False

    photo_path = os.path.join(PHOTO_FOLDER, f"{roll_no}_{name}.jpg")
    capture_photo(photo_path)

    image = face_recognition.load_image_file(photo_path)
    face_locations = face_recognition.face_locations(image)
    no_of_Faces = len(face_locations)

    if no_of_Faces != 1:
        os.remove(photo_path)
        return f"There should be one face, {no_of_Faces} detected", False
    
    return f"Student {name} registered successfully!", True

def mark_attendance(roll_no):
    """Marks attendance by verifying the student."""
    if not roll_no:
        return "Roll number is required!", False
    
    try:
        roll_no=int(roll_no)
    except ValueError:
        return "Roll no should be Integer", False

    # Capture the current photo
    temp_photo = "temp_photo.jpg"
    capture_photo(temp_photo)

    # Match the photo
    for file in os.listdir(PHOTO_FOLDER):
        if file.startswith(str(roll_no) + "_"):
            saved_photo_path = os.path.join(PHOTO_FOLDER, file)
            saved_image = face_recognition.load_image_file(saved_photo_path)
            saved_encoding = face_recognition.face_encodings(saved_image)[0]

            temp_image = face_recognition.load_image_file(temp_photo)
            temp_encodings = face_recognition.face_encodings(temp_image)
            
            if temp_encodings:
                matches = face_recognition.compare_faces(temp_encodings, saved_encoding ,tolerance=TOLERENCE)
                if True in matches:
                    name = file.split("_")[1].replace(".jpg", "")
                    log_attendance(roll_no, name)
                    os.remove(temp_photo)
                    return "Attendance marked successfully!", True

    os.remove(temp_photo)
    return "Face not recognized or matched!", False

def log_attendance(roll_no, name):
    """Logs attendance to the CSV file."""
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    
    # Add new attendance entry
    with open(ATTENDANCE_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([roll_no, name, date, time])

def get_attendance_data():
    with open(ATTENDANCE_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        data = []
        next(reader)
        for row in reader:
            data.append(row)

        return data
