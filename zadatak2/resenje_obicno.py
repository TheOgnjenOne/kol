import pandas as pd

# ==========================================
# 1. UCITAVANJE PODATAKA
# ==========================================
try:
    df_top100 = pd.read_csv('spotify_alltime_top100_songs.csv')
    df_artists_2025 = pd.read_csv('spotify_wrapped_2025_top50_artists.csv')
    df_songs_2025 = pd.read_csv('spotify_wrapped_2025_top50_songs.csv')
except FileNotFoundError as e:
    print(f"Greska: Proveri da li su CSV fajlovi u istom folderu kao i skripta! \n{e}")
    exit()

# ==========================================
# 2. OSNOVNA INSPEKCIJA (za svaki DF)
# ==========================================
dfs = {
    "ALL TIME TOP 100": df_top100,
    "2025 TOP 50 ARTISTS": df_artists_2025,
    "2025 TOP 50 SONGS": df_songs_2025
}

for name, df in dfs.items():
    print(f"\n{'='*10} ANALIZA: {name} {'='*10}")
    print(f"Prvih 5 redova:\n{df.head()}\n")
    print(f"Kolone: {df.columns.tolist()}")
    print(f"Prazne celije:\n{df.isnull().sum()}")
    print(f"Tipovi podataka:\n{df.dtypes}\n")

# ==========================================
# 3. ANALIZA: TOP 50 ARTISTS 2025
# ==========================================
print("\n--- SPECIFICNI ZADACI: ARTISTS 2025 ---")

# 1. Pop izvodjaci
pop_artists = df_artists_2025[df_artists_2025['genre'].str.contains('Pop', case=False, na=False)]

# 2. Prebrojati zanrove
genre_counts = df_artists_2025['genre'].value_counts()

# 3. Top 5 drzava
top_countries = df_artists_2025['country'].value_counts().head(5)

# 4. Sortiranje po Grammy nagradama
grammy_sorted = df_artists_2025.sort_values(by='grammy_awards', ascending=False)

# 5. Ispod 20m pratilaca
less_than_20m = df_artists_2025[df_artists_2025['followers'] < 20000000]

# 6. Grupisanje po genderu i 7. Prosek Grammy-a
avg_grammy_gender = df_artists_2025.groupby('gender')['grammy_awards'].mean()
print(f"Prosek Grammy nagrada po polu:\n{avg_grammy_gender}")

# ==========================================
# 4. ANALIZA: TOP 50 SONGS 2025
# ==========================================
print("\n--- SPECIFICNI ZADACI: SONGS 2025 ---")

# 1. Top 5 izvodjaca po broju pesama
top_artist_count = df_songs_2025['artist'].value_counts().head(5)

# 2. Ukupni strimovi po izvodjacu
sum_streams = df_songs_2025.groupby('artist')['streams'].sum()

# 3. Prosek BPM po zanru (i za pesme sa vise zanrova)
df_songs_exploded = df_songs_2025.copy()
df_songs_exploded['genre'] = df_songs_exploded['genre'].str.split('_') # pretpostavka separatora _
df_songs_exploded = df_songs_exploded.explode('genre')
avg_bpm_genre = df_songs_exploded.groupby('genre')['bpm'].mean()

# 4. Sortiranje po godini
songs_2025_sorted = df_songs_2025.sort_values(by='release_year')

# 5. Prosek danceability po zanru
avg_dance_genre = df_songs_exploded.groupby('genre')['danceability'].mean()

# 6. Top 5 acousticness
top_acoustic = df_songs_2025.nlargest(5, 'acousticness')

# 7. Broj pojavljivanja drzava
country_song_counts = df_songs_2025['country'].value_counts()

# ==========================================
# 5. ANALIZA: TOP 100 ALL TIME
# ==========================================
print("\n--- SPECIFICNI ZADACI: TOP 100 ALL TIME ---")

# 1. Sortiranje po godini
top100_sorted = df_top100.sort_values(by='release_year')

# 2. Prosek acousticness po zanru
avg_acoustic_alltime = df_top100.groupby('genre')['acousticness'].mean()

# 3. Broj pesama po dekadi
df_top100['decade'] = (df_top100['release_year'] // 10) * 10
decade_stats = df_top100['decade'].value_counts().sort_index()

# 4. Pop Rock izvodjaci
pop_rock_artists = df_top100[df_top100['genre'].str.contains('Pop Rock', case=False)]['artist'].unique()

# 5. Eksplicitni izvodjaci
explicit_artists = df_top100[df_top100['is_explicit'] == True]['artist'].unique()

# 6. Sortiranje po BPM
bpm_sorted_alltime = df_top100.sort_values(by='bpm')

# 7. Dueti (izvodjaci koji imaju separator u imenu)
duets = df_top100[df_top100['artist'].str.contains('feat|&|,', case=False)]

# ==========================================
# 6. PRESEK LISTA (DODATNO)
# ==========================================
# Provera koje pesme iz 2025 su vec u Top 100 All Time
common_songs = pd.merge(df_songs_2025, df_top100, on=['track_name', 'artist'], how='inner')

print("\n--- REZULTAT PRESEKA ---")
if not common_songs.empty:
    print(f"Pronadjeno pesama: {len(common_songs)}")
    print(common_songs[['track_name', 'artist']])
else:
    print("Nijedna pesma iz 2025 se ne nalazi na All Time listi.")