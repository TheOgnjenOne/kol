import pandas as pd
import numpy as np

# Pravimo testni primer
data = {
    'naziv': ['  Bohemian Rhapsody  ', 'In the End', 'Shape of You', 'Believer', np.nan],
    'zanr': ['Rock', 'Nu-metal', 'Pop', 'Rock', 'Unknown'],
    'info': ['Legendary;Old', 'Rap;Rock', 'Modern;Pop', 'Modern;Rock', 'N/A']
}
df = pd.DataFrame(data)

# ============================================================
# 1. PRETRAGA I FILTRIRANJE
# ============================================================

# contains - Da li tekst sadrzi podstring (najbitnija komanda)
rock_filmovi = df[df['zanr'].str.contains('rock', case=False, na=False)]

# startswith / endswith - Provera pocetka ili kraja
pocinje_sa_b = df[df['naziv'].str.startswith('B', na=False)]
zavrsava_sa_u = df[df['naziv'].str.endswith('u', na=False)]

# isin - Provera da li je vrednost tacno jedna od ponudjenih u listi
specificni = df[df['zanr'].isin(['Pop', 'Rock'])]

# ============================================================
# 2. ČIŠĆENJE I TRANSFORMACIJA
# ============================================================

# strip - Brise razmake na pocetku i kraju (vazno kod ucitavanja txt/csv)
df['naziv'] = df['naziv'].str.strip()

# lower / upper - Prebacivanje u mala ili velika slova
df['zanr_mala'] = df['zanr'].str.lower()
df['zanr_velika'] = df['zanr'].str.upper()

# replace - Zamena dela teksta
df['info'] = df['info'].str.replace(';', ' | ')

# ============================================================
# 3. RAD SA VIŠESTRUKIM VREDNOSTIMA (Listama)
# ============================================================

# split - Razbija string u listu na osnovu separatora
# Rezultat: ['Legendary', 'Old']
df['info_lista'] = df['info'].str.split('|')

# explode - "Razvaljuje" listu tako da svaki element dobije svoj red
# Ako je pesma imala 2 zanra, sad ces imati 2 reda za tu pesmu (idealno za prosek)
df_prosirun = df.explode('info_lista')

# ============================================================
# 4. INFORMACIJE O TEKSTU
# ============================================================

# len - Broj karaktera u ćeliji
df['duzina_naziva'] = df['naziv'].str.len()

# count - Koliko puta se odredjeni karakter pojavljuje
# npr. koliko zanrova ima (broji separatore)
df['broj_tagova'] = df['info'].str.count('\|') + 1

# ============================================================
# 5. ISECANJE (Slicing)
# ============================================================

# Prva tri slova naziva
df['kod'] = df['naziv'].str[:3]

print("Obradjeni podaci:")
print(df)