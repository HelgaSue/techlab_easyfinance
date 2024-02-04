import tkinter as tk

from cobag_kontoauszug import import_cobag
from cobacc_kontoauszug import import_cobacc
from ksk_kontoauszug import import_ksk
from kategorisierung import kategorisiere_transaktion, load_keywords_from_csv
from visualisierung import summe_kategorien, create_piechart, summe_kategorien_linienchart, create_linechart


file_path = r"C:\Users\Florian\OneDrive\Techlabs 2023\keywords.CSV"  # Pfad zur CSV-Datei mit Keywords
# erstellen des main windows
root = tk.Tk()
root.title("Um was für einen Kontoauszug handelt es sich?")

root.geometry('800x400')

frame = tk.Frame(root)
frame.pack(pady=20)
# erstellen eines labels um result darzustellen
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack(pady=20)

selected_function = None
categories = []

kategorien = load_keywords_from_csv(file_path)
categories = list(kategorien.keys())
# Dictionary um funktionen namen zu funktionen zu mappen
function_mapping = {
    "import_cobag": import_cobag,
    "import_ksk": import_ksk,
    "import_cobacc": import_cobacc, 
}

options = [
    ("Kreissparkasse", "import_ksk"),
    ("Commerzbank Girokonto", "import_cobag"),
    ("Commerzbank Visa", "import_cobacc"), 
]

# Funktion, um alle Widgets im Frame zu löschen
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()

def show_bank_options():
    clear_frame()  # Vorherige Widgets löschen
    for option_text, function_name in options:
        option_button = tk.Button(frame, text=option_text, command=lambda f=function_name: option_selected(f))
        option_button.pack(pady=10)
    # hinzufügen des zurück buttons
    back_button = tk.Button(frame, text="Zurück", command=show_bank_options)
    back_button.pack(pady=10)
    back_button.pack_forget()  # Macht den zurück Button unsichtbar, wird in 1. Übersicht nicht benötigt

# Aufrufen von show_bank_options beim Start des Programms
show_bank_options()

# Funktion, um die Chart-Auswahl-Buttons anzuzeigen
def show_chart_options():
    clear_frame()  # Vorherige Buttons löschen
    tk.Button(frame, text="Pie Chart", command=show_pie_chart).pack(pady=10)
    tk.Button(frame, text="Line Chart", command=show_line_chart_options).pack(pady=10)
    # zeigt den zurück Button an
    tk.Button(frame, text="Zurück", command=show_bank_options).pack(pady=10)

def option_selected(selected_function_name):
    global selected_function
    try:
        if selected_function_name in function_mapping:
            selected_function = function_mapping[selected_function_name]
            show_chart_options()  # zeigt die Optionen für Pie und Line Chart
        else:
            result_label.config(text=f"{selected_function_name} has no associated function.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

def show_pie_chart():
    try:
        # aufrufen der bankfunktion um die daten zu bekommen
        result = selected_function()
         
        # summe der Kategorien für den Pie Chart
        category_totals, oberkategorie_totals = summe_kategorien(process_result(result))
        
        # erstellung des Pie Chart
        create_piechart(category_totals, oberkategorie_totals)

    except Exception as e:
        result_label.config(text=f"Error: {e}")
       

def process_result(result):
    processed_transactions = []
    for index, transaction in enumerate(result):
        verwendungszweck = transaction[2]  
        betrag = transaction[1]            
        empfänger = transaction[3]
        # führt die kategorisierung durch
        kategorie, oberkategorie = kategorisiere_transaktion(verwendungszweck, betrag, empfänger, kategorien)
        
        processed_transaction = transaction + [kategorie, oberkategorie]
        processed_transactions.append(processed_transaction)
    return processed_transactions 
        #print(transaction) -> überprüfen ob daten richtig übergeben

def show_line_chart_options():
    clear_frame()  
    # sortiert die kategorien alphabetisch
    sorted_categories = sorted(categories)
    
    # erstellt Checkbuttons für jede Kategorie und positioniert die in einem 4x4-Muster
    rows, cols = 4, 4  
    for i, category in enumerate(sorted_categories):
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(frame, text=category, variable=var)
        checkbox.var = var
        checkbox.grid(row=i // cols, column=i % cols, sticky='w')  
    
    # fügt den Button zum Erzeugen des Line Charts hinzu
    tk.Button(frame, text="Generate Line Chart", command=generate_line_chart).grid(row=rows, column=0, columnspan=cols, pady=10)
    # zeigt den zurück Button an
    tk.Button(frame, text="Zurück", command=show_bank_options).grid(row=rows+1, column=0, columnspan=cols, pady=10)


def generate_line_chart():
    selected_categories = [checkbox.cget("text") for checkbox in frame.winfo_children() if isinstance(checkbox, tk.Checkbutton) and checkbox.var.get()]
    result = selected_function()
    processed_transactions = process_result(result) 
    grouped_data = summe_kategorien_linienchart(processed_transactions, selected_categories)
    create_linechart(grouped_data)

# startet den main loop
root.mainloop()

