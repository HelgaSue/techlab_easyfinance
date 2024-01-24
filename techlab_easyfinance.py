# Main file for our project
import csv 
import re
import tkinter as tk

# Function to handle button clicks
def option_selected(option):
    result_label.config(text=f'You selected: {option}')

# Create the main window
root = tk.Tk()
root.title("Um was für einen Kontoauszug handelt es sich?")

# Create a label to display the result
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=20)

# Create buttons for different options
options = ["Kreissparkasse", "Commerzbank Griokonto", "Commerzbank Visa"]

for option in options:
    option_button = tk.Button(root, text=option, command=lambda o=option: option_selected(o))
    option_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
