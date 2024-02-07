def import_ksk():
    
    # Path to the Account Statement file
    file_path = 'KSK.CSV'

    # Open the CSV file and read it
    with open(file_path, 'r', encoding='iso-8859-1') as account_statement:

        csv_reader = csv.reader(account_statement, delimiter=';')

        # Skip the header row
        header = next(csv_reader, None)

        # Accumulate all values in a single list
        all_values = []

        # Define a regular expression pattern for a Credit Card entry (Master Card)
        pattern = re.compile(r'MASTER CARD [^ ]+ (.+?) \d{2}\.\d{2}\.\d{4}')

        # Initialize the incomes and the expenditures
        sum_expenditures = 0
        sum_incomes = 0

        # Iterate through each row
        for row in csv_reader:
            # Check if the row is not empty
            if row:
                # Extract values from columns date, type, description, amount
                date = row[1]
                type = row[3]
                verwendungszweck = row[4]
                amount = round(float(row[14].replace(',', '.')), 2) 

                # Check if 'MASTER CARD' is in the description and extract the useful information
                if 'MASTER CARD' in verwendungszweck:
                    match = re.search(pattern, verwendungszweck)
                    if match:
                        extracted_characters = match.group(1).lower()

                        # Create a list with values
                        values_list = [date, type, extracted_characters, amount]
                        # Update the sum for incomes and expenditures 
                        if amount < 0:
                            sum_expenditures += amount
                        if amount > 0:
                            sum_incomes += amount
                else:
                    # For rows where 'MASTER CARD' is not in the description
                    values_list = [date, type, verwendungszweck, amount]
                    # Update the sum for incomes and expenditures 
                    if amount < 0:
                        sum_expenditures += amount
                    if amount > 0:
                        sum_incomes += amount

                # Append the values to the single list
                all_values.append(values_list)
