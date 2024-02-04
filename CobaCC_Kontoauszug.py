import csv

def import_cobacc():
    file_path = r"C:\Users\Florian\OneDrive\Techlabs 2023\CC.csv"
    bank_data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            buchungsdatum = row['\ufeffBuchungstag']
            betrag = float(row['Betrag'].replace(',', '.'))
            verwendungszweck = row['Buchungstext']
            
            verwendungszweck_words = verwendungszweck.split()
            
            # Nimm nur die ersten beiden Wörter/Zahlen, wenn vorhanden
            modified_verwendungszweck = ' '.join(verwendungszweck_words[:2])
            # Setze empfaenger basierend auf dem Betrag
            if betrag > 0:
                empfaenger = "ich"
            else:
                # Nimm die ersten zwei Wörter des Verwendungszwecks als Empfänger
                empfaenger = ' '.join(verwendungszweck_words[:2])
          
            values_list = [buchungsdatum, betrag, modified_verwendungszweck, empfaenger] # oberkategorie, kategorie
            bank_data.append(values_list)
        return bank_data
    
sorted_statement = import_cobacc()
