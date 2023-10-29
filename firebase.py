import tkinter as tk
from tkinter import ttk
import pyrebase

# Firebase configuration
firebase_config = {
  "apiKey": "AIzaSyAu3wkOx1iSbiye_eJspq-xr-Idj-g3dnk",
  "authDomain": "gsr-89764.firebaseapp.com",
  "databaseURL": "https://gsr-89764-default-rtdb.firebaseio.com",
  "projectId": "gsr-89764",
  "storageBucket": "gsr-89764.appspot.com",
  "messagingSenderId": "146150740629",
  "appId": "1:146150740629:web:dac0946b4ab39bec28419c",
  "measurementId": "G-VC4HF0YYBY"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Create the Tkinter app
root = tk.Tk()
root.title("Raspberry Pi Firebase GUI")

# Calculate the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - 800) // 2 
y = (screen_height - 600) // 2  
root.geometry(f"800x600+{x}+{y}")

# Function to fetch data from Firebase and update the label text
def fetch_data():
    data_path = "users/month1/day1/gsr"
    data = db.child(data_path).get().val()
    if data is not None:
        data_label.config(text=f"Data: {data}")
        update_status(data)
    else:
        data_label.config(text="Data not found")

def update_status(data):
    global above_threshold_count, below_threshold_count

    if data >= 400:
        above_threshold_count += 1
        below_threshold_count = 0
        if above_threshold_count >= 30:
            status_label.config(text="Dehydrated", font=("Arial", 24, "bold"), foreground="red")
        else:
            status_label.config(text="Mildly Dehydrated", font=("Arial", 16), foreground="orange")
    elif data <= 200:
        below_threshold_count += 1
        above_threshold_count = 0
        if below_threshold_count >= 30:
            status_label.config(text="Fully Hydrated", font=("Arial", 24, "bold"), foreground="green")
        else:
            status_label.config(text="Mildly Dehydrated", font=("Arial", 16), foreground="orange")
    else:
        above_threshold_count = 0
        below_threshold_count = 0
        status_label.config(text="Mildly Dehydrated", font=("Arial", 16), foreground="orange")

def update_data():
    fetch_data()
    root.after(5000, update_data)

def exit_application():
    root.destroy()

# Create GUI elements
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Change background color and text color
frame["style"] = "My.TFrame"
style = ttk.Style()
style.configure("My.TFrame", background="#EAEAEA") 
style.configure("TButton", foreground="white", background="#007ACC") 
style.configure("TLabel", background="#EAEAEA", foreground="black")  

# Center the frame components
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Title label
title_label = ttk.Label(frame, text="Realtime Data from Firebase", font=("Helvetica", 24, "bold"))
title_label.pack(pady=20, anchor="center")

# Data label
data_label = ttk.Label(frame, text="Data: ", font=("Helvetica", 18))
data_label.pack(pady=10, anchor="center")

# Status label
status_label = ttk.Label(frame, text="Status: Mildly Dehydrated", font=("Helvetica", 16))
status_label.pack(pady=10, anchor="center")

# Quit button
quit_button = ttk.Button(frame, text="Quit", command=exit_application)
quit_button.pack(anchor="center")

# Initialize counters for consecutive readings above and below thresholds
above_threshold_count = 0
below_threshold_count = 0

# Start the GUI main loop
root.after(0, update_data)
root.mainloop()
