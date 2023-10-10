import pymongo
import base64
import numpy as np
import cv2
import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import os

# Connect to MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["FaceRecognition"]
image_collection = db["image"]

# Create a Tkinter window
root = tk.Tk()
root.title("Retrieve Image")

# Set the window size
root.geometry("300x200")

# Get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the Tkinter window to appear in the middle of the screen
x = int((screen_width / 2) - (300 / 2))
y = int((screen_height / 2) - (200 / 2))

# Set the Tkinter window to appear in the middle of the screen
root.geometry(f"300x200+{x}+{y}")


# Create label and input widgets for date and time
date_label = tk.Label(root, text="Enter date (YYYY-MM-DD): ", width=30)
date_label.pack(pady = 5)
date_entry = tk.Entry(root, width=30)
date_entry.pack(pady = 5)

time_label = tk.Label(root, text="Enter time (HH:MM:SS): ", width=30)
time_label.pack(pady = 5)
time_entry = tk.Entry(root, width=30)
time_entry.pack(pady = 5)

def retrieve_image():
    # Get user input for date and time
    date = date_entry.get()
    time = time_entry.get()

    # Convert date and time to timestamp
    timestamp = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S.%f")

    # Retrieve the image based on timestamp
    image_record = image_collection.find_one({"timestamp": timestamp})

    # Check if image exists for the given timestamp
    if image_record is None:
        messagebox.showerror("Error", "No image found for the given date and time.", parent=root)
    else:
        # Extract image data from the image record
        image_data = image_record["image"]
        try:
            image_binary = base64.b64decode(image_data)
            image_np = np.frombuffer(image_binary, dtype=np.uint8)
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
        except:
            messagebox.showerror("Error", "The retrieved image is corrupted.", parent=root)
            return

        # Print the dimensions of the image
        print("Image dimensions:", image.shape)

        # Save the retrieved image to a file
        file_name = f"{date}.png"
        dataset_dir = filedialog.askdirectory()
        full_path = os.path.join(dataset_dir, file_name)

        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        print("Current working directory:", os.getcwd())
        print("Saving image to:", full_path)
        with open(full_path, 'wb') as f:
            f.write(image_binary)

        messagebox.showinfo("Success", f"Image saved to {full_path}.")


# Create a button widget to retrieve image
retrieve_button = tk.Button(root, text="Retrieve Image", command=retrieve_image)
retrieve_button.pack(pady = 5)

# Configure the root window to have a fixed size
root.geometry("300x200")

# Start the Tkinter event loop
root.mainloop()

















