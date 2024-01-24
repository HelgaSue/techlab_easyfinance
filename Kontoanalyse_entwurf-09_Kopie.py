import csv
from datetime import datetime
import pandas as pd

# Funktion zum Laden von Transaktionen aus einer CSV-Datei
def load_transactions(csv_file):
    with open(csv_file, newline='', encoding='ISO-8859-1') as file:
        reader = csv.DictReader(file)
        transactions = list(reader)
    return transactions


# Funktion zur Auswahl aus einer Liste von Optionen
def choose_from_list(prompt, options):
    while True:
      #zeigt eine Liste von Optionen an, die der Benutzer auswählen kann
        print(prompt)
        for i, option in enumerate(options, start=1): #nummeriert die liste
            print(f"{i}. {option}")

        #Benutzer gibt die Nummer der Auswahl ein, und die Funktion gibt die ausgewählte Option zurück.
        choice = input("Gib die Nummer der Auswahl ein: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
            else:
                print("Ungültige Auswahl. Versuche es erneut.")
        except ValueError:
            print("Ungültige Eingabe. Bitte gib eine Zahl ein.")


# Hauptfunktion zur Filterung und Summierung von Transaktionen. Sie interagiert mit dem Benutzer,
# um eine CSV-Datei zu laden, einen Zeitraum festzulegen, Buchungsarten und Verwendungszwecke auszuwählen,
# Transaktionen zu filtern, Einnahmen und Ausgaben zu berechnen und schließlich eine Zusammenfassung anzuzeigen.
def filter_and_sum_transactions():
  #Überspringe die Initialisierung von Variablen
    csv_file = None
    transactions = None
    start_date = None
    end_date = None

    while True:
        # Benutzereingabe für die CSV-Datei
        if csv_file is None or input("Möchtest du eine neue bzw. andere CSV-Datei laden (aus dem gleichen Dateipfad)? (ja/nein): ").lower() == 'ja':
            csv_file = input("Gib den CSV-Dateinamen ein: ")
            transactions = load_transactions(csv_file)

            # Zeige DataFrame-Ausschnitt
            display_part_dataframe(transactions)

        # Benutzereingabe für den Zeitraum
        if start_date is None or end_date is None or input("Möchtest du einen neuen bzw. anderen Zeitraum festlegen? (ja/nein): ").lower() == 'ja':
            start_date_str = input("Gib das Startdatum im Format JJJJ-MM-TT ein: ")
            end_date_str = input("Gib das Enddatum im Format JJJJ-MM-TT ein: ")

            try:
                # Konvertiere die Benutzereingabe in datetime-Objekte
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                print("Ungültiges Datumsformat. Verwende das Format JJJJ-MM-TT.")
                continue

        # Erstelle Auswahlliste für Buchungsart und lass den Benutzer auswählen
        available_transaction_types = list(get_unique_values_in_range(transactions, 'Transaktionsart', start_date, end_date))
        transaction_type = choose_from_list("Gib die Transaktionsart ein:", available_transaction_types)

        # Erstelle Auswahlliste für Verwendungszweck basierend auf der ausgewählten Transaktionsart
        available_purposes = list(get_unique_values_in_range(transactions, 'Verwendungszweck', start_date, end_date, 'Transaktionsart', transaction_type))

        # Liste die Verwendungszwecke auf inkl. Nummerierung
        print(f"Verwendungszwecke für die Buchungsart '{transaction_type}':")
        for i, purpose in enumerate(available_purposes, start=1):
            print(f"{i}. {purpose}")

        # Frage nach Zusammenführung
        merge_purposes = input("Möchtest du Verwendungszwecke zusammenführen? (ja/nein): ").lower() == 'ja'

        # Falls der Benutzer Verwendungszwecke zusammenführen möchte
        if merge_purposes:
            while True:
                # Lasse den Benutzer die Nummern der Verwendungszwecke eingeben
                purpose_indices_str = input("Gib die Nummern der Verwendungszwecke (durch Komma getrennt) ein: ")
                purpose_indices = purpose_indices_str.split(',')

                try:
                    # Umwandlung Benutzereingabe in eine Liste von Indexen
                    selected_purposes = [available_purposes[int(index) - 1] for index in purpose_indices]
                    break
                except (ValueError, IndexError):
                    print("Ungültige Eingabe. Bitte gib die Nummern erneut ein.")

            # Filtere Transaktionen nach dem angegebenen Zeitraum, Transaktionsart und ausgewählten Verwendungszwecken
            filtered_transactions = [t for t in transactions if (
                start_date is None or start_date <= datetime.strptime(t['Buchungsdatum'], '%Y-%m-%d') <= end_date
                and t['Transaktionsart'] == transaction_type
                and t['Verwendungszweck'].lower() in [purpose.lower() for purpose in selected_purposes]
            )]
        else:
            # Benutzereingabe von die Nummer des Verwendungszwecks
            while True:
                purpose_index_str = input("Gib die Nummer des Verwendungszwecks ein (leer lassen, wenn nicht relevant): ")
                if purpose_index_str == '':
                    purpose = ''
                    break

                try:
                    # Umwandlung der Benutzereingabe in den Index
                    purpose_index = int(purpose_index_str) - 1
                    purpose = available_purposes[purpose_index]
                    break
                except (ValueError, IndexError):
                    print("Ungültige Eingabe. Bitte gib die Nummer erneut ein.")

            # Filtere Transaktionen nach dem angegebenen Zeitraum, Buchungsart und ausgewähltem Verwendungszweck
            filtered_transactions = [t for t in transactions if (
                start_date is None or start_date <= datetime.strptime(t['Buchungsdatum'], '%Y-%m-%d') <= end_date
                and t['Transaktionsart'] == transaction_type
                and (purpose == '' or t['Verwendungszweck'].lower() == purpose.lower())
            )]

        # Initialisiere Variablen für Einnahmen, Ausgaben und Gesamtsumme
        income = 0
        expense = 0

        # Iteriere durch die gefilterten Transaktionen und aktualisiere Einnahmen und Ausgaben
        for transaction in filtered_transactions:
            amount = float(transaction['Betrag (EUR)'])
            if amount >= 0:
                income += amount
            else:
                expense += abs(amount)

        # Berechne die Gesamtsumme
        total = income - expense

        # Erstellung eines DataFrame für die Ergebnisse
        result_df = pd.DataFrame({
            'Buchungsdatum': [t['Buchungsdatum'] for t in filtered_transactions],
            'Transaktionsart': [t['Transaktionsart'] for t in filtered_transactions],
            'Verwendungszweck': [t['Verwendungszweck'] for t in filtered_transactions],
            'Betrag (EUR)': [float(t['Betrag (EUR)']) for t in filtered_transactions]
        })

        # Anzeige das Ergebnis DataFrames
        print("\nErgebnis DataFrame:")
        print(result_df)

        # Anzeige der Zusammenfassung
        print("\nZusammenfassung:")
        print(f"Transaktionen im Zeitraum: {start_date_str} bis {end_date_str}")
        print(f"Transaktionsart: {transaction_type}")
        print(f"ausgewählte Verwendungszweck(e): {', '.join(selected_purposes) if merge_purposes else purpose}")
        print(f"Einnahmen: {income:.2f} EUR")
        print(f"Ausgaben: {expense:.2f} EUR")
        print(f"Gesamt: {total:.2f} EUR")

        # Frage nach weiterer Analyse
        another_analysis = input("Möchtest du eine weitere Analyse durchführen? (ja/nein): ").lower()

        # Wenn der Benutzer keine weitere Analyse durchführen möchte, beende das Programm
        if another_analysis != 'ja':
            print("Das Programm wird beendet. Auf Wiedersehen!")
            break

# Funktion erstellt einen Teil-DataFrame (part_df) aus den übergebenen Daten und zeigt ihn an.
def display_part_dataframe(data):
    # Erstelle einen DataFrame-Ausschnitt
    part_df = pd.DataFrame(data)

    # Zeige das DataFrame an
    print("\nDataFrame Ausschnitt:")
    print(part_df)

# Funktion extrahiert eindeutige Werte für einen bestimmten Schlüssel (key) innerhalb eines Zeitraums (definiert durch start_date und end_date).
# Optional kann sie auch nach einem zusätzlichen Schlüssel-Wert-Paar (filter_key und filter_value) filtern.
def get_unique_values_in_range(data, key, start_date, end_date, filter_key=None, filter_value=None):
    if filter_key and filter_value is not None:
        return set(item[key] for item in data if start_date <= datetime.strptime(item['Buchungsdatum'], '%Y-%m-%d') <= end_date and item[filter_key] == filter_value)
    else:
        return set(item[key] for item in data if start_date <= datetime.strptime(item['Buchungsdatum'], '%Y-%m-%d') <= end_date)

# Hauptfunktion
# Eingabeaufforderung: Benutzereingabe für Zeitraum, Transaktionsart und Verwendungszweck
filter_and_sum_transactions()
