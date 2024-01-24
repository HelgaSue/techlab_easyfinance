def create_bank_data(file_path):
    raw_data = import_CobaGiro(file_path)
    bank_data = []

    for row in raw_data:

        kategorie, oberkategorie = kategorisiere_transaktion(row['Verwendungszweck'], row['Betrag'])
        verwendungszweck = row['Verwendungszweck'].lower()
        bank_data.append({'Buchungsdatum': row['Buchungsdatum'], 'Betrag': row['Betrag'], 'Verwendungszweck': verwendungszweck, 'Empfänger': row['Empfänger'], 'Oberkategorie': oberkategorie, 'Kategorie': kategorie})

    return bank_data
