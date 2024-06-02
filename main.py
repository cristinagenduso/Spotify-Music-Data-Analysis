# In[1]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# In[2]
tracks = pd.read_csv('./inputs/saved_tracks_with_audio_features.csv')

# In[3]
tracks.head()

# In[4]
pd.isnull(tracks).sum()

# In[5]
tracks.info()

# In[6]
# Display the top 10 tracks with the highest popularity
most = tracks.sort_values(by='Popularity', ascending=False).head(10)
print(most[['Name', 'Artists', 'Popularity']])

# In[7]
# Display summary statistics of the numerical columns in the dataset
tracks.describe().transpose()

# In[8]
# Calculate the average popularity of tracks
average_popularity = tracks['Popularity'].mean()
print(f'Average Popularity: {average_popularity}')

# In[9]
# Select numerical columns for correlation analysis
numeric_columns = tracks.select_dtypes(include=['float64', 'int64']).columns

td = tracks[numeric_columns].corr(method = 'pearson')
plt.figure(figsize=(9,5))
hmap = sns.heatmap(td, annot = True, fmt = '.1g', vmin=-1, vmax=1, center=0, cmap='crest', linewidths=0.1, linecolor='black')
hmap.set_title('Correlation HeatMap')
hmap.set_xticklabels(hmap.get_xticklabels(), rotation=90)

# In[11]
# Plot the regression between 'Acousticness' and 'Popularity'
sns.set_style('darkgrid')
plt.figure(figsize=(10, 6))

sns.regplot(data=tracks, x='Acousticness', y='Popularity', color='orange').set(title='Popularity vs Acousticness Correlation')
plt.show()

# In[12]
# Extract and count all genres
all_genres = []
for genres in tracks['Genres']:
    genresList = genres.split(", ")
    all_genres.extend(genresList)

genre_counts = pd.Series(all_genres).value_counts()

# Plot the top 5 genres by frequency
plt.figure(figsize=(5, 5))
popular = genre_counts.sort_values(ascending=False).head(5)
sns.barplot(y=popular.index, x=popular.values, palette='viridis', legend=False).set(title='Top 5 Genres by Frequency')
plt.ylabel("")
plt.show()

# In[13]
# Extract the month from the 'Added At' column
tracks['Added At'] = pd.to_datetime(tracks['Added At'])
tracks['Month'] = tracks['Added At'].dt.month_name().str[:3]

# Count the number of track additions per month
monthly_additions = tracks['Month'].value_counts().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Plot the monthly additions of favorite tracks
plt.figure(figsize=(12, 8))
sns.barplot(x=monthly_additions.index, y=monthly_additions.values, palette='flare')
plt.title('Monthly Additions of Favorite Tracks')
plt.ylabel('Number of Tracks Added')
plt.xlabel("")
plt.show()

# In[14]
# Filter tracks with genres containing 'indie'
indie_tracks = tracks[tracks['Genres'].str.contains('indie', case=False, na=False)]
daily_indie_additions = indie_tracks['Added At'].dt.date.value_counts().sort_index()

# Plot the daily additions of indie tracks
plt.figure(figsize=(14, 7))
sns.lineplot(x=daily_indie_additions.index, y=daily_indie_additions.values, marker='o', color='fuchsia')
plt.title('Days with Peaks of Indie Tracks')
plt.ylabel('Number of Indie Tracks Added')
plt.xlabel("")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# In[15]
# Count the number of tracks by top 5 indie artists
indie_artists = indie_tracks['Artists'].str.split(',').explode().value_counts().head(5)

# Plot the top 5 artists
plt.figure(figsize=(12, 8))
sns.barplot(y=indie_artists.index, x=indie_artists.values, palette='cubehelix')
plt.title('Top Indie Artists')
plt.xlabel('')
plt.ylabel('')
plt.show()