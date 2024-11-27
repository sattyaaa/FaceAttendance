import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import attendance  # Import functions from the attendance.py file

# GUI Setup
root = tk.Tk()
root.title("Facial Recognition Attendance System")
root.geometry("600x400")

frames = {}

def switch_frame(frame):
    """Switches to the given frame."""
    for f in frames.values():
        f.pack_forget()  # Hide all frames
    frame.pack(fill="both", expand=True)  # Show the selected frame

def create_label_and_entry(frame, label_text):
    """Create a label and entry field in the given frame."""
    tk.Label(frame, text=label_text).pack()
    entry = tk.Entry(frame)
    entry.pack()
    return entry

def create_button(frame, text, command):
    """Create a button in the given frame."""
    tk.Button(frame, text=text, command=command, width=20).pack(pady=10)

# Function to clear the fields
def clear_fields(entry_widgets):
    """Clears all the entry fields provided in the list."""
    for entry in entry_widgets:
        entry.delete(0, tk.END)

# Main Menu Frame
main_menu = tk.Frame(root)
frames["main_menu"] = main_menu

tk.Label(main_menu, text="Attendance System", font=("Arial", 18)).pack(pady=20)
create_button(main_menu, "Register", lambda: switch_frame(frames["register"]))
create_button(main_menu, "Mark Attendance", lambda: switch_frame(frames["mark_attendance"]))
create_button(main_menu, "View Attendance", lambda: switch_frame(frames["view_attendance"]))

# Register Frame
register_frame = tk.Frame(root)
frames["register"] = register_frame

tk.Label(register_frame, text="Register Student", font=("Arial", 16)).pack(pady=10)
roll_no_entry = create_label_and_entry(register_frame, "Roll No:")
name_entry = create_label_and_entry(register_frame, "Name:")

def on_register():
    """Handles the register button click."""
    roll_no = roll_no_entry.get()
    name = name_entry.get()
    result = attendance.register_student(roll_no, name)
    if result[1] == True:
        messagebox.showinfo("Success", result[0])
        clear_fields([roll_no_entry, name_entry])  # Clear the fields after successful registration
    else:
        messagebox.showerror("Error", result[0])

create_button(register_frame, "Capture & Register", on_register)
create_button(register_frame, "Back", lambda: switch_frame(main_menu))

# Mark Attendance Frame
mark_frame = tk.Frame(root)
frames["mark_attendance"] = mark_frame

tk.Label(mark_frame, text="Mark Attendance", font=("Arial", 16)).pack(pady=10)
roll_no_entry_mark = create_label_and_entry(mark_frame, "Roll No:")

def on_mark_attendance():
    """Handles the mark attendance button click."""
    roll_no = roll_no_entry_mark.get()
    result = attendance.mark_attendance(roll_no)
    if result[1] == True:
        messagebox.showinfo("Success", result[0])
        roll_no_entry_mark.delete(0, tk.END)  # Clear the roll number field after marking attendance
    else:
        messagebox.showerror("Error", result[0])

create_button(mark_frame, "Capture & Mark Attendance", on_mark_attendance)
create_button(mark_frame, "Back", lambda: switch_frame(main_menu))

# View Attendance Frame
view_frame = tk.Frame(root)
frames["view_attendance"] = view_frame

tk.Label(view_frame, text="Attendance Details", font=("Arial", 16)).pack(pady=10)

# Create Treeview for displaying attendance data
tree = ttk.Treeview(view_frame, columns=("Roll No", "Name", "Date", "Time"), show="headings")

# Configure column headings
tree.heading("Roll No", text="Roll No", anchor="center")
tree.heading("Name", text="Name", anchor="center")
tree.heading("Date", text="Date", anchor="center")
tree.heading("Time", text="Time", anchor="center")

# Configure column widths and center the data
tree.column("Roll No", width=20, anchor="center")
tree.column("Name", width=60, anchor="center")
tree.column("Date", width=50, anchor="center")
tree.column("Time", width=50, anchor="center")

tree.pack(fill="both", expand=True, padx=10, pady=10)


def populate_attendance_table():
    """Populates the Treeview with attendance data."""
    data = attendance.get_attendance_data()  # Fetch the data from your CSV file
    for row in tree.get_children():
        tree.delete(row)  # Clear existing data
    for record in data:
        tree.insert("", "end", values=record)

create_button(view_frame, "Refresh", populate_attendance_table)
create_button(view_frame, "Back", lambda: switch_frame(main_menu))

# Start the GUI
switch_frame(main_menu)
root.mainloop()
