def kategorisiere_transaktion(verwendungszweck, betrag):
    kategorien = {
        'Miete': {'keywords': ['miete', 'studierendenwerk', 'wohnheim', 'rent']},
        'Einkauf': {'keywords': ['einkauf', 'kauf', 'shopping']},
        'Gehalt': {'keywords': ['gehalt', 'lohn', 'entgelt']},
        'OnlineEinkauf': {'keywords': ['amazon', 'paypal', 'ebay']},
        'LaufendeKosten': {'keywords': ['gas', 'wasser', 'stadtwerke']},
        'Versicherungen': {'keywords': ['versicherung']},
        'Kreditkarten': {'keywords': ['barclays', 'visa', 'kreditkarte']},
        'Sonstiges': {'keywords': []}
    }
    # konvertieren des formates des Verwendungszwecks in Kleinbuchstaben, um zu filtern
    verwendungszweck_klein = verwendungszweck.lower()

    # Bestimme, ob es sich um eine Einnahme oder Ausgabe handelt
    oberkategorie = 'Einnahmen' if not betrag.startswith('-') else 'Ausgaben'

    # Überprüfe jede Kategorie
    for kategorie, data in kategorien.items():
        if any(keyword in verwendungszweck_klein for keyword in data['keywords']):
            if kategorie and betrag.startswith('-'):
                return kategorie, oberkategorie
            elif kategorie and not betrag.startswith('-'):
                return kategorie, oberkategorie
    return 'Sonstiges', oberkategorie  # Rückgabewert, wenn keine Übereinstimmung gefunden wird

