import tkinter as tk

from cobag_kontoauszug import import_cobag
from cobacc_kontoauszug import import_cobacc
from ksk_kontoauszug import import_ksk
from kategorisierung import kategorisiere_transaktion, load_keywords_from_csv

file_path = r"C:\Users\Florian\OneDrive\Techlabs 2023\keywords.CSV"  # Pfad zur CSV-Datei mit Keywords
kategorien = load_keywords_from_csv(file_path)
# Create the main window
root = tk.Tk()
root.title("Um was für einen Kontoauszug handelt es sich?")

# Create a label to display the result
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=20)

# Dictionary to map function names to actual functions
function_mapping = {
    "import_cobag": import_cobag,
    "import_ksk": import_ksk,
    "import_cobacc": import_cobacc, 
}



# Function to handle button clicks and execute the selected function
def option_selected(selected_function_name):
    try:
        # Execute the selected function
        if selected_function_name in function_mapping:
            selected_function = function_mapping[selected_function_name]
            result = selected_function()  # Call the function and capture the return value
            
            # Handle or display the result
            # result_label.config(text=f"Result from {selected_function_name}: {result}")
            
            # If you want to do something with the result, you can add your code here
            process_result(result)
        else:
            result_label.config(text=f"{selected_function_name} has no associated function.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")
# Create buttons for different options
        
options = [
    ("Kreissparkasse", "import_ksk"),
    ("Commerzbank Girokonto", "import_cobag"),
    ("Commerzbank Visa", "import_cobacc"), 
]
def process_result(result):
    for index, transaction in enumerate(result):
        verwendungszweck = transaction[2]  # Get 'Verwendungszweck'
        betrag = transaction[1]            # Get 'Betrag'
        empfänger = transaction[3]
        # Führen Sie die Kategorisierung durch
        kategorie, oberkategorie = kategorisiere_transaktion(verwendungszweck, betrag, empfänger, kategorien)
        
        # Aktualisieren Sie die Transaktion in der Ergebnisliste mit Kategorie und Oberkategorie
        transaction.extend([kategorie, oberkategorie])
        result[index] = transaction
        print(transaction)
for option_text, function_name in options:
    option_button = tk.Button(root, text=option_text, command=lambda f=function_name: option_selected(f))
    option_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
