import pandas as pd
import plotly.express as px

# 0. Učitavanje
df = pd.read_csv('../spotify_alltime_top100_songs.csv')
df.columns = df.columns.str.lower().str.strip()

# 1. Top 5 (Bar, Pie, Treemap)
top5 = df.nlargest(5, 'total_streams_billions')
px.bar(top5, x='song_title', y='total_streams_billions', title="Top 5 Bar").show()
px.pie(top5, values='total_streams_billions', names='song_title', title="Top 5 Pie").show()
px.treemap(top5, path=['song_title'], values='total_streams_billions', title="Top 5 Treemap").show()

# 2. Scatter: Danceability vs Energy
px.scatter(df, x='danceability', y='energy', size='total_streams_billions', color='release_year', hover_name='song_title').show()

# 3. Histogram: Godine
px.histogram(df, x='release_year', nbins=20, title="Godine nbins=20").show()
px.histogram(df, x='release_year', nbins=50, title="Godine nbins=50").show()

# 4. Pie: Explicit
px.pie(df, names='explicit', title="Explicit udeo").show()

# 5. Line: Strimovi po godinama
st_god = df.groupby('release_year')['total_streams_billions'].sum().reset_index()
px.line(st_god, x='release_year', y='total_streams_billions').show()

# 6. Box: BPM po žanru
px.box(df, x='primary_genre', y='bpm').show()

# 7. Box: BPM Top 10 žanrova
top10_genres = df['primary_genre'].value_counts().nlargest(10).index
df_t10 = df[df['primary_genre'].isin(top10_genres)]
px.box(df_t10, x='primary_genre', y='bpm').show()

# 8. Scatter: Acousticness vs Valence
px.scatter(df, x='acousticness', y='valence', color='artist_country', size='total_streams_billions').show()

# 9. Heatmap
px.imshow(df.select_dtypes(include=['number']).corr(), text_auto=True).show()

# 10. 3D Scatter
px.scatter_3d(df, x='energy', y='valence', z='danceability', color='primary_genre', size='total_streams_billions').show()