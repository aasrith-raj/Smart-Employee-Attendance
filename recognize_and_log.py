import tkinter as tk
from tkinter import Toplevel, Label, Button
import cv2
from PIL import Image, ImageTk
import face_recognition
import numpy as np
import datetime
import os
import csv
from geolocation import get_location

known_face_encodings = []
known_face_names = []

def load_known_faces():
    global known_face_encodings, known_face_names
    dataset_dir = "dataset"
    for filename in os.listdir(dataset_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(dataset_dir, filename)
            image = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(image)
            if encoding:
                known_face_encodings.append(encoding[0])
                emp_id, name_ext = filename.split("_", 1)
                name = name_ext.rsplit(".", 1)[0]
                known_face_names.append(name)

def log_to_csv(timestamp, name, latitude, longitude):
    file_path = "database.csv"
    file_exists = os.path.exists(file_path)

    with open(file_path, mode="a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "Name", "Latitude", "Longitude"])
        writer.writerow([timestamp, name, latitude, longitude])

def show_custom_message(title, message, fg="black", on_close=None):
    msg_win = Toplevel()
    msg_win.title(title)
    msg_win.geometry("400x180")
    msg_win.configure(bg="#f0f8ff")

    Label(msg_win, text=title, font=("Arial", 14, "bold"), bg="#f0f8ff", fg=fg).pack(pady=(20, 10))
    Label(msg_win, text=message, font=("Arial", 11), bg="#f0f8ff").pack(pady=(0, 20))

    def handle_close():
        msg_win.destroy()
        if on_close:
            on_close()

    Button(msg_win, text="OK", width=12, font=("Arial", 10), bg="#4CAF50", fg="white",
           command=handle_close).pack()

def show_retry_message(title, message, fg, retry_callback, cancel_callback):
    msg_win = Toplevel()
    msg_win.title(title)
    msg_win.geometry("400x200")
    msg_win.configure(bg="#f0f8ff")

    Label(msg_win, text=title, font=("Arial", 14, "bold"), bg="#f0f8ff", fg=fg).pack(pady=(20, 10))
    Label(msg_win, text=message, font=("Arial", 11), bg="#f0f8ff").pack(pady=(0, 20))

    btn_frame = tk.Frame(msg_win, bg="#f0f8ff")
    btn_frame.pack()

    Button(btn_frame, text="Retry", width=12, font=("Arial", 10), bg="#2196F3", fg="white",
           command=lambda: [msg_win.destroy(), retry_callback()]).pack(side="left", padx=10)

    Button(btn_frame, text="Cancel", width=12, font=("Arial", 10), bg="#F44336", fg="white",
           command=lambda: [msg_win.destroy(), cancel_callback()]).pack(side="right", padx=10)

class AttendanceApp:
    def __init__(self, master):
        self.window = Toplevel(master)
        self.window.title("Mark Attendance")

        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = None
        self.face_locations = []
        self.face_encodings = []
        self.process_this_frame = True

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.take_button = tk.Button(self.window, text="Take Attendance", width=30, command=self.capture_and_log)
        self.take_button.pack(pady=10)

        load_known_faces()
        self.delay = 15
        self.update()

        self.logged_names = set()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update(self):
        ret, frame = self.video_capture.read()
        if ret:
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            if self.process_this_frame:
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.process_this_frame = not self.process_this_frame

            for (top, right, bottom, left), face_encoding in zip(self.face_locations, self.face_encodings):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            self.current_frame = frame
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            self.canvas.imgtk = imgtk
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)

        self.window.after(self.delay, self.update)

    def reset_for_retry(self):
        self.face_encodings = []
        self.face_locations = []

    def capture_and_log(self):
        if not self.face_encodings:
            show_custom_message("Result", "No face detected.", fg="red")
            return

        new_logs = 0
        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            if name != "Unknown" and name not in self.logged_names:
                self.logged_names.add(name)
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                try:
                    location = get_location()
                    latitude = location.get('latitude', 'N/A')
                    longitude = location.get('longitude', 'N/A')
                except Exception:
                    latitude = "Unavailable"
                    longitude = "Unavailable"

                log_to_csv(timestamp, name, latitude, longitude)
                new_logs += 1

        if new_logs > 0:
            show_custom_message(
                "Success",
                "Attendance logged to database.csv",
                fg="green",
                on_close=self.window.destroy
            )
        else:
            show_retry_message(
                "Result",
                "No recognized face or already logged.",
                fg="orange",
                retry_callback=self.reset_for_retry,
                cancel_callback=self.window.destroy
            )

    def on_closing(self):
        self.video_capture.release()
        self.window.destroy()

def run_attendance_app():
    AttendanceApp(tk._default_root)
