import csv


def load_keywords_from_csv(file_path):
    kategorien = {}
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            kategorie = row['category']
            keywords = row['keywords'].split('|')
            kategorien[kategorie] = {'keywords': keywords}
    return kategorien

def kategorisiere_transaktion(verwendungszweck, betrag, empfänger, kategorien):
    verwendungszweck_klein = verwendungszweck.lower()
    empfaenger_klein = empfänger.lower()
    oberkategorie = 'Einnahmen' if betrag > 0 else 'Ausgaben'

    for kategorie, data in kategorien.items():

        if any(keyword in verwendungszweck_klein for keyword in data['keywords']):

            return kategorie, oberkategorie
        
        if any(keyword in empfaenger_klein for keyword in data['keywords']):

            return kategorie, oberkategorie
        
# Wenn keine passende Kategorie gefunden wurde, überprüft Oberkategorie
    if oberkategorie == 'Ausgaben':
        return 'Sonstige Ausgaben', oberkategorie
    elif oberkategorie == 'Einnahmen':
        return 'Sonstige Einnahmen', oberkategorie

    # Wenn weder Kategorie noch Oberkategorie übereinstimmen, fällt es in "Sonstiges"
    return 'Sonstiges', oberkategorie        
