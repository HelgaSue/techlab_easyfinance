import csv
import re


def import_cobag():
    file_path = r"CoBa.csv"
    bank_data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            buchungsdatum = row['\ufeffBuchungstag']
            betrag = float(row['Betrag'].replace(',', '.'))
            verwendungszweck = row['Buchungstext']
            empfaenger = "ich" if betrag > 0 else re.split(r'\d', verwendungszweck, 1)[0].strip()
           
            modified_verwendungszweck = extract_modified_purpose(verwendungszweck)
            values_list = [buchungsdatum, betrag, modified_verwendungszweck, empfaenger] # oberkategorie, kategorie
            bank_data.append(values_list)
        return bank_data
    
def extract_modified_purpose(text):
    # Schneidet den Text an der Stelle "End-to-End-Ref" ab, falls vorhanden
    end_to_end_ref_index = text.find('End-to-End-Ref')
    if end_to_end_ref_index != -1:
        text_before_end_to_end = text[:end_to_end_ref_index].strip()
        # extrahiert den Text nach der letzten Zahl vor "End-to-End-Ref"
        match = re.search(r'\d+(.*)', text_before_end_to_end)
        if match:
            after_number_to_end_to_end = match.group(1).strip()
            # überprüfen, ob Text zwischen ersten Zahl und "End-to-End-Ref" nur aus Zahlen besteht
            if re.search('[a-zA-Z]', after_number_to_end_to_end):
                # Wenn Buchstaben vorhanden sind, verwenden Sie diesen Teil
                return after_number_to_end_to_end
            else:
                # wenn keine Buchstaben vorhanden sind, verwendet Text vor der ersten Zahl
                return text_before_end_to_end[:match.start()].strip()
        else:
            return text_before_end_to_end
    else:
        # wenn "End-to-End-Ref" nicht vorhanden ist, verwendet Text vor der ersten Zahl
        match = re.split(r'\d', text, 1)
        return match[0].strip() if match else text
sorted_statement = import_cobag()
