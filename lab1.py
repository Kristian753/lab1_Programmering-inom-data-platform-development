import pandas as pd
import numpy as np
import os

# hämta aktuell scripts mappsökväg
current_dir = os.path.dirname(os.path.abspath(__file__))
# skapa fullständig sökväg till CSV
csv_path = os.path.join(current_dir, 'lab 1 - csv.csv')

# läs in csv som DataFrame
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

# rensa blanksteg i kolumnnamn
df.columns = df.columns.str.strip()
# rensa blanksteg i produktnamn
df['name'] = df['name'].str.strip()
# rensa blanksteg i valuta
df['currency'] = df['currency'].str.strip()

# konvertera pris till numeriskt värde
df['price_clean'] = pd.to_numeric(df['price'].replace('free', '0'), errors='coerce')

# konvertera datum till datetime-format
df['date_clean'] = pd.to_datetime(df['created_at'], errors='coerce')

# flagga negativt pris
df['negativt_pris'] = df['price_clean'] < 0 
# flagga felaktiga datum                   
df['fel_datum'] = df['date_clean'].isna()    
# flagga saknade id och namn                  
df['saknar_id'] = df['id'].isna()  
# flagga saknade namn                            
df['saknar_namn'] = df['name'].isna()                          

# markera rader som ska bort
df['ta_bort'] = df['negativt_pris'] | df['fel_datum'] | df['saknar_id'] | df['saknar_namn']

# filtrera fram giltiga rader
bra_data = df[df['ta_bort'] == False].copy()
# beräkna medelvärde för pris
snittpris = bra_data['price_clean'].mean() 
# beräkna medianpris                    
medianpris = bra_data['price_clean'].median()      
# räkna antal giltiga produkter          
antal_produkter = len(bra_data)  
# räkna antal produkter utan pris                              
antal_saknat_pris = bra_data['price_clean'].isna().sum()       


# Här skapar vi en dictionary med all information
summary_data = {
    'variabel': ['snittpris', 'medianpris', 'antal produkter', 'antal produkter med saknat pris'],
    'värde': [
        round(snittpris, 2) if pd.notna(snittpris) else 0,     # Avrunda till 2 decimaler
        round(medianpris, 2) if pd.notna(medianpris) else 0,   # Avrunda till 2 decimaler
        antal_produkter,                                        # Antal produkter (heltal)
        antal_saknat_pris                                       # Antql utan pris (heltal)
    ]
}

# spara sammanfattning till ny CSV
pd.DataFrame(summary_data).to_csv('analytics_summary.csv', index=False)

print("analytics_summary.csv filen har skapats")