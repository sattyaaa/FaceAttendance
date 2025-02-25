import sqlite3

def create_connection():
    """Create a database connection and return the connection object."""
    conn = sqlite3.connect('attendance.db')
    return conn

def create_table():
    """Create the student and attendance tables if they do not exist."""
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS student (
                    roll_no INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    face_encoding BLOB NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    roll_no INTEGER,
                    date_time TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (roll_no) REFERENCES student(roll_no)
                )''')
    conn.commit()
    conn.close()

# Ensure tables are created
create_table()