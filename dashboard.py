import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import sys
import pandas as pd
import os

root = tk.Tk()

root.title("Face Attendance System")

root.geometry("700x500")

root.configure(bg="#1e293b")


title = tk.Label(
    root,
    text="🎓 FACE ATTENDANCE SYSTEM",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#1e293b"
)

title.pack(pady=30)


# ---------------- REGISTER ----------------

def register_student():

    subprocess.Popen(
        [sys.executable, "student_register.py"]
    )


# ---------------- ATTENDANCE ----------------

def start_attendance():

    subprocess.Popen(
        [sys.executable, "app.py"]
    )


# ---------------- VIEW CSV (TABLE + PHOTO PREVIEW) ----------------

PHOTO_FOLDER = os.path.join("attendance", "Photos")


def view_attendance():

    file = "attendance/attendance.csv"

    if not os.path.exists(file):

        messagebox.showerror(
            "Error",
            "Attendance file not found"
        )

        return

    df = pd.read_csv(file)

    win = tk.Toplevel()
    win.title("Attendance Records")
    win.geometry("950x500")
    win.configure(bg="#1e293b")

    # ---- LEFT: Table ----

    table_frame = tk.Frame(win, bg="#1e293b")
    table_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    columns = list(df.columns)

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---- RIGHT: Photo preview ----

    preview_frame = tk.Frame(win, bg="#1e293b", width=300)
    preview_frame.pack(side="right", fill="y", padx=10, pady=10)

    preview_label = tk.Label(
        preview_frame,
        text="Click a row\nto see photo",
        bg="#1e293b",
        fg="white",
        font=("Arial", 12)
    )
    preview_label.pack(expand=True)

    # Keep a reference so the image isn't garbage collected
    preview_label.image_ref = None

    def on_row_select(event):

        selected = tree.focus()

        if not selected:
            return

        values = tree.item(selected, "values")

        if not values:
            return

        # "Photo" column value
        try:
            photo_index = columns.index("Photo")
        except ValueError:
            preview_label.config(text="No 'Photo' column found", image="")
            return

        photo_name = values[photo_index]
        photo_path = os.path.join(PHOTO_FOLDER, photo_name)

        if not photo_name or not os.path.exists(photo_path):
            preview_label.config(text="Photo not found", image="")
            preview_label.image_ref = None
            return

        try:
            img = Image.open(photo_path)
            img.thumbnail((280, 280))
            photo_img = ImageTk.PhotoImage(img)

            preview_label.config(image=photo_img, text="")
            preview_label.image_ref = photo_img  # prevent garbage collection

        except Exception as e:
            preview_label.config(text=f"Error loading photo:\n{e}", image="")
            preview_label.image_ref = None

    tree.bind("<<TreeviewSelect>>", on_row_select)


# ---------------- EXIT ----------------

def exit_app():

    root.destroy()


# BUTTON STYLE

btn_width = 25
btn_height = 2  


tk.Button(
    root,
    text="➕ Register Student",
    command=register_student,
    width=btn_width,
    height=btn_height,
    bg="#22c55e",
    fg="white"
).pack(pady=10)


tk.Button(
    root,
    text="📷 Start Attendance",
    command=start_attendance,
    width=btn_width,
    height=btn_height,
    bg="#3b82f6",
    fg="white"
).pack(pady=10)


tk.Button(
    root,
    text="📊 View Attendance",
    command=view_attendance,
    width=btn_width,
    height=btn_height,
    bg="#f59e0b",
    fg="white"
).pack(pady=10)


tk.Button(
    root,
    text="❌ Exit",
    command=exit_app,
    width=btn_width,
    height=btn_height,
    bg="#ef4444",
    fg="white"
).pack(pady=10)


root.mainloop()