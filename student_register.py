import cv2
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

os.makedirs("dataset", exist_ok=True)

root = tk.Tk()
root.withdraw()

name = simpledialog.askstring(
    "Register Student",
    "Enter Student Name:"
)

if name:

    cap = cv2.VideoCapture(0)

    messagebox.showinfo(
        "Capture",
        "Press OK and look at camera.\nPhoto will capture automatically in 3 seconds."
    )

    for i in range(90):
        ret, frame = cap.read()

        cv2.putText(
            frame,
            f"Capturing in {3 - i//30}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        cv2.imshow("Register Student", frame)

        cv2.waitKey(1)

    path = f"dataset/{name}.jpg"

    cv2.imwrite(path, frame)

    cap.release()
    cv2.destroyAllWindows()

    messagebox.showinfo(
        "Success",
        f"{name} Registered Successfully!"
    )