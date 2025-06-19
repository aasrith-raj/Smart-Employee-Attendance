from tkinter import Tk, Button, Label, messagebox, Toplevel, Frame
import recognize_and_log
import register_faces
import os

def get_employees():
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        return []
    return [f for f in os.listdir(dataset_dir) if f.endswith(".jpg") or f.endswith(".png")]

def show_employee_list():
    employees = get_employees()
    
    list_window = Toplevel()
    list_window.title("Registered Employees")
    list_window.geometry("400x400")
    list_window.configure(bg="#f0f8ff")

    Label(list_window, text="Registered Employees", font=("Helvetica", 14, "bold"),
          bg="#f0f8ff", fg="#333").pack(pady=15)

    content_frame = Frame(list_window, bg="#f0f8ff")
    content_frame.pack(fill='both', expand=True)

    if not employees:
        Label(content_frame, text="No employees registered.",
              font=("Arial", 12), bg="#f0f8ff", fg="red").pack(pady=20)
    else:
        for emp_file in employees:
            try:
                emp_id, name_ext = emp_file.split("_", 1)
                name = name_ext.rsplit(".", 1)[0]
                Label(content_frame, text=f"ID: {emp_id} | Name: {name}",
                      font=("Arial", 11), bg="#f0f8ff", anchor='w').pack(fill='x', padx=20, pady=2)
            except ValueError:
                Label(content_frame, text=f"Unrecognized: {emp_file}",
                      font=("Arial", 11), bg="#f0f8ff", fg="gray").pack(fill='x', padx=20, pady=2)

def styled_button(master, text, command, x, y, bg="#4CAF50", fg="white", hover_bg="#45a049"):
    def on_enter(e):
        btn['background'] = hover_bg
    def on_leave(e):
        btn['background'] = bg

    btn = Button(master, text=text, command=command, width=25, height=2,
                 font=("Arial", 11, "bold"), bg=bg, fg=fg, bd=0, relief='flat')
    btn.place(x=x, y=y)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def launch_gui():
    root = Tk()
    root.title("Face Attendance System")
    root.geometry("680x600")
    root.configure(bg="#ffffff")

    Label(root, text="Welcome to Attendance System", font=("Arial", 16, "bold"),
          bg="#ffffff", fg="#003366").place(x=180, y=50)

    # Position buttons centrally with vertical spacing
    styled_button(root, "Mark Attendance", recognize_and_log.run_attendance_app, x=220, y=150,
                  bg="#2196F3", hover_bg="#1E88E5")
    styled_button(root, "Register New Employee", register_faces.register_face, x=220, y=220,
                  bg="#FF9800", hover_bg="#FB8C00")
    styled_button(root, "Show Employee List", show_employee_list, x=220, y=290,
                  bg="#9C27B0", hover_bg="#8E24AA")
    styled_button(root, "Exit", root.quit, x=220, y=360,
                  bg="#F44336", hover_bg="#E53935")

    root.mainloop()

if __name__ == "__main__":
    launch_gui()
