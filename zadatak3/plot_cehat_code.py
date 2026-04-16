import pandas as pd
import plotly.express as px
import numpy as np

# =================================================================
# 1. PANDAS OSNOVE - KAKO "PRIČATI" SA TABELOM
# =================================================================

# Učitavanje (Uvek kreni odavde)
df = pd.read_csv('spotify_alltime_top100_songs.csv')

# --- Brzi uvid ---
df.head()          # Prvih 5 redova
df.info()          # Tipovi podataka i da li ima praznih (non-null)
df.describe()      # Statistika (prosek, min, max) za brojeve
df.columns         # Spisak svih kolona

# --- Filtriranje ---
# Nadji sve pesme gde je 'streams' veci od milijardu
popularne = df[df['streams'] > 1000000000]

# --- Grupisanje (Zlatna komanda za ispite) ---
# "Izracunaj prosek BPM-a za svaki zanr"
# .reset_index() dodajemo da bi rezultat ostao u formi tabele (DataFrame)
prosek_bpm = df.groupby('genre')['bpm'].mean().reset_index()

# --- Sortiranje ---
# Sortiraj po godini od najnovije ka najstarijoj
df_sorted = df.sort_values(by='release_year', ascending=False)


# =================================================================
# 2. STRING OPERACIJE (.str) - ČIŠĆENJE PODATAKA
# =================================================================

# Najvaznije opcije za pretragu teksta:
# case=False -> Ne gleda velika/mala slova (Pop == pop)
# na=False   -> Preskace prazna polja bez pucanja greske

# contains: Da li tekst sadrzi rec (npr. trazi Rock u zanrovima)
rock_songs = df[df['genre'].str.contains('Rock', case=False, na=False)]

# strip: Brise nevidljive razmake na pocetku/kraju (bitno za fajlove!)
df['track_name'] = df['track_name'].str.strip()

# split i explode: Ako jedan red ima vise zanrova razdvojenih sa "_"
# 1. Split napravi listu: "Pop_Rock" -> ["Pop", "Rock"]
# 2. Explode napravi nove redove: jedan za Pop, jedan za Rock
df['genre_list'] = df['genre'].str.split('_')
df_detaljno = df.explode('genre_list')


# =================================================================
# 3. PLOTLY VIZUELIZACIJA - PRAVILA I FUNKCIJE
# =================================================================

"""
OPŠTA PRAVILA ZA PLOTLY:
1. Prvi argument je uvek DataFrame (df).
2. x, y, color, size su uvek IMENA KOLONA pod navodnicima.
3. .show() je obavezan na kraju.
"""

# --- BAR (Poređenje) ---
# Prikazi top 5 pesama po strimovima
top5 = df.nlargest(5, 'streams')
fig_bar = px.bar(top5, x='track_name', y='streams', color='artist', title="Top 5 Pesama")
# fig_bar.show()

# --- PIE (Udeli u procentima) ---
# Udeo eksplicitnih pesama (kolona 'is_explicit')
fig_pie = px.pie(df, names='is_explicit', title="Udeo Explicit pesama")
# fig_pie.show()

# --- SCATTER (Korelacija / Odnos dve stvari) ---
# x i y su ose, size je velicina tacke, color je boja po kategoriji
fig_scatter = px.scatter(df, x='energy', y='danceability', 
                         size='streams', color='genre', 
                         hover_name='track_name')
# fig_scatter.show()

# --- HISTOGRAM (Distribucija / Koliko necega ima) ---
# nbins=20 znaci "podeli godine u 20 stubica"
fig_hist = px.histogram(df, x='release_year', nbins=20, title="Pesme kroz godine")
# fig_hist.show()

# --- BOX PLOT (Statisticki raspon i autlajeri) ---
# Idealno za BPM, Energy ili Danceability po zanrovima
fig_box = px.box(df, x='genre', y='bpm', color='genre')
# fig_box.show()

# --- HEATMAP (Korelacija svih brojeva) ---
# Prvo izracunaj korelaciju (.corr), pa je ubaci u imshow
numeric_cols = df.select_dtypes(include='number')
korelacija_tabele = numeric_cols.corr()
fig_heatmap = px.imshow(korelacija_tabele, text_auto=True, title="Mapa korelacija")
# fig_heatmap.show()


# =================================================================
# 4. KRATKA UPUTSTVA ZA POKRETANJE
# =================================================================
"""
KAKO POKRENUTI:
1. Instaliraj biblioteke: pip install pandas plotly
2. Postavi .csv fajl u isti folder gde je i ovaj .py fajl.
3. Pokreni skriptu. Svaki .show() ce otvoriti novi tab u tvom Chrome/Edge browseru.

SAVETI:
- Ako grafikon nece da se ucita, proveri imena kolona (da li je 'Artist' ili 'artist').
- Za Line Chart UVEK prvo uradi .groupby() jer linija ne moze da ide kroz 100 razlicitih tacaka za istu godinu.
- nbins u histogramu: sto je veci broj, to su stubici tanji i precizniji.
"""