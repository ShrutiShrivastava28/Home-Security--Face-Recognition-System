import tkinter as tk
import os
import subprocess
from tkinter import messagebox
from PIL import ImageTk, Image

# Function to execute the training.py file
def train_model():
    subprocess.call(["python", "Training.py"])
    messagebox.showinfo("Training", "Training is done")

# Function to execute the recognize.py file
def recognize_faces():
    script_path = os.path.join(os.getcwd(), "Recognize.py")
    subprocess.Popen(["python", "Recognize.py"])

# Function to execute the retrieve.py file
def retrieve_images():
    script_path = os.path.join(os.getcwd(), "retriveimage.py")
    subprocess.Popen(["python", "retriveimage.py"])

# Create the GUI window
window = tk.Tk()
window.title("AI Face Recognition System")

# Function to handle button clicks
def button_click(file):
    if file == "train":
        train_model()
    elif file == "recognize":
        recognize_faces()
    elif file == "retrieve":
        retrieve_images()

# Set the window size
window.geometry("500x400")

# Get the screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the x and y coordinates for the Tkinter window to appear in the middle of the screen
x = int((screen_width / 2) - (500 / 2))
y = int((screen_height / 2) - (400 / 2))

# Set the Tkinter window to appear in the middle of the screen
window.geometry(f"500x400+{x}+{y}")

# Create and place the buttons
train_button = tk.Button(window, text="Training", command=lambda: button_click("train"), width=30, height=5)
train_button.pack(pady=20)

recognize_button = tk.Button(window, text="Recognize", command=lambda: button_click("recognize"), width=30, height=5)
recognize_button.pack(pady=20)

retrieve_button = tk.Button(window, text="Retrieve", command=lambda: button_click("retrieve"), width=30, height=5)
retrieve_button.pack(pady=20)

# Function to execute the sound.py file
def play_sound():
    subprocess.Popen(["python", "sound.py"])

# Load the bell icon image
bell_icon = ImageTk.PhotoImage(Image.open("bell_icon.png"))

# Create the bell button with the icon
bell_button = tk.Button(window, image=bell_icon, command=play_sound)
bell_button.place(x=20, y=20, width=49, height=49)

# Start the GUI event loop
window.mainloop()

