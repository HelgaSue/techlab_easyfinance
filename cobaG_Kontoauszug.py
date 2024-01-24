def import_CobaGiro(file_path):
    bank_data = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for row in reader:
            buchungsdatum = row['\ufeffBuchungstag']
            betrag = row['Betrag']
            verwendungszweck = row['Buchungstext']
            if float(betrag.replace(',','.')) < 0:
                empfaenger = verwendungszweck.split()[0]
            elif float(betrag.replace(',','.')) > 0:
                empfaenger = "ich"
            verwendungszweck = re.split(r'\d', verwendungszweck, 1)[0].strip()
            bank_data.append({'Buchungsdatum': buchungsdatum, 'Betrag': betrag, 'Verwendungszweck': verwendungszweck, 'Empfänger': empfaenger})

    return bank_data

