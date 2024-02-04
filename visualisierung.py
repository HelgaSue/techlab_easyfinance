from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as ple

def summe_kategorien(transactions):
    # erstellt ein Pandas DataFrame aus den Transaktionsdaten
    df = pd.DataFrame(transactions, columns=['Buchungsdatum', 'Betrag', 'Verwendungszweck', 'Empfänger', 'Kategorie', 'Oberkategorie'])

    # filtert die Daten nach Oberkategorien
    ausgaben_df = df[df['Oberkategorie'] == 'Ausgaben']
    einnahmen_df = df[df['Oberkategorie'] == 'Einnahmen']

    # berechnet die Summen der Kategorien für Ausgaben und Einnahmen
    ausgaben_sum = ausgaben_df.groupby('Kategorie')['Betrag'].sum().reset_index().round(2)
    einnahmen_sum = einnahmen_df.groupby('Kategorie')['Betrag'].sum().reset_index().round(2)

    return ausgaben_sum, einnahmen_sum

def create_piechart(ausgaben_sum, einnahmen_sum):
    # Ausgaben Tortendiagramm
    plt.figure(figsize=(10, 6))
    plt.pie(ausgaben_sum['Betrag'].abs(), labels=None, autopct=lambda p: '{:.2f}%'.format(p) if p > 1 else '', pctdistance=0.85)
    plt.title('Verteilung der Ausgaben nach Kategorien')
    # Legende hinzufügen
    plt.legend(ausgaben_sum['Kategorie'], loc="best", bbox_to_anchor=(1, 1))
    plt.axis('equal')  
    plt.show()
    
    # Einnahmen Tortendiagramm
    plt.figure(figsize=(10, 6))
    plt.pie(einnahmen_sum['Betrag'].abs(), labels=None, autopct=lambda p: '{:.2f}%'.format(p) if p > 1 else '', pctdistance=0.85)
    plt.title('Verteilung der Einnahmen nach Kategorien')
    # Legende hinzufügen
    plt.legend(einnahmen_sum['Kategorie'], loc="best", bbox_to_anchor=(1, 1))
    plt.axis('equal') 
    plt.show()

def summe_kategorien_linienchart(transactions, selected_categories=None):
    df = pd.DataFrame(transactions, columns=['Buchungsdatum', 'Betrag', 'Verwendungszweck', 'Empfänger', 'Kategorie', 'Oberkategorie'])
    df['Buchungsdatum'] = pd.to_datetime(df['Buchungsdatum'])
    # beträge in Absolutwerte umwandeln (mit negativ nicht sinnvoll)
    df['Betrag'] = df['Betrag'].abs()
    grouped_df = df.groupby([pd.Grouper(key='Buchungsdatum', freq='M'), 'Kategorie']).sum().reset_index()

    # filtern, wenn Kategorien ausgewählt
    if selected_categories is not None:
        grouped_df = grouped_df[grouped_df['Kategorie'].isin(selected_categories)]

    return grouped_df

def create_linechart(grouped_df):
    fig, ax = plt.subplots(figsize=(12, 6))
    for kategorie in grouped_df['Kategorie'].unique():
        df_kategorie = grouped_df[grouped_df['Kategorie'] == kategorie]
        ax.plot(df_kategorie['Buchungsdatum'], df_kategorie['Betrag'], label=kategorie)
    ax.set_xlabel('Datum')
    ax.set_ylabel('Betrag')
    ax.set_title('Ausgaben und Einnahmen über die Zeit')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
