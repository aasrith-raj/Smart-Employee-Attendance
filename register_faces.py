import cv2
import os
from tkinter import Toplevel, Label, Button, Entry, messagebox, Frame, BOTH, BOTTOM, X
from PIL import Image, ImageTk
import face_recognition

DATASET_DIR = "dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

def register_face():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    window = Toplevel()
    window.title("Register New Employee")
    window.geometry("750x750")
    window.configure(bg="#f0f8ff")

    Label(window, text="Employee Registration", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)

    form_frame = Frame(window, bg="#f0f8ff")
    form_frame.pack(pady=5)

    Label(form_frame, text="Employee ID:", font=("Arial", 11), bg="#f0f8ff").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    emp_id_entry = Entry(form_frame, width=30)
    emp_id_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(form_frame, text="Employee Name:", font=("Arial", 11), bg="#f0f8ff").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    name_entry = Entry(form_frame, width=30)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    panel_frame = Frame(window, bg="#f0f8ff", height=480)
    panel_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    panel_frame.pack_propagate(False)

    panel = Label(panel_frame)
    panel.pack()

    captured = False
    snapshot_frame = [None]

    def update_frame():
        if not cap.isOpened():
            return

        ret, frame = cap.read()
        if not ret:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)

        for (top, right, bottom, left) in faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        panel.imgtk = imgtk
        panel.config(image=imgtk)

        snapshot_frame[0] = frame.copy()

        window.after(15, update_frame)

    def show_retry_cancel_popup():
        msg_win = Toplevel(window)
        msg_win.title("No Face Detected")
        msg_win.geometry("400x200")
        msg_win.configure(bg="#f0f8ff")

        Label(msg_win, text="Error", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="red").pack(pady=(20, 10))
        Label(msg_win, text="No face detected.\nWould you like to retry or cancel?", font=("Arial", 11),
              bg="#f0f8ff").pack(pady=(0, 20))

        btn_frame = Frame(msg_win, bg="#f0f8ff")
        btn_frame.pack()

        def retry():
            nonlocal captured
            captured = False
            msg_win.destroy()

        def cancel():
            cap.release()
            cv2.destroyAllWindows()
            msg_win.destroy()
            window.destroy()

        Button(btn_frame, text="Retry", width=12, font=("Arial", 10), bg="#2196F3", fg="white",
               command=retry).pack(side="left", padx=10)

        Button(btn_frame, text="Cancel", width=12, font=("Arial", 10), bg="#F44336", fg="white",
               command=cancel).pack(side="right", padx=10)

    def capture_face():
        nonlocal captured
        emp_id = emp_id_entry.get().strip()
        name = name_entry.get().strip()

        if not emp_id or not name:
            messagebox.showerror("Input Error", "Please enter both Employee ID and Name.")
            return

        captured = True
        frame = snapshot_frame[0]

        if frame is None:
            messagebox.showerror("Error", "No frame captured.")
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)

        if not faces:
            show_retry_cancel_popup()
        else:
            filename = f"{emp_id}_{name}.jpg"
            path = os.path.join(DATASET_DIR, filename)
            cv2.imwrite(path, frame)
            messagebox.showinfo("Success", f"Employee {name} registered successfully.")
            cap.release()
            cv2.destroyAllWindows()
            window.destroy()

    Button(window, text="Capture & Register", font=("Arial", 12, "bold"),
           bg="#4CAF50", fg="white", command=capture_face).pack(side=BOTTOM, fill=X, pady=15)

    update_frame()
