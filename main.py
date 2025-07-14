import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load the dataset
df = pd.read_csv("netflix_titles.csv")

# Show first few rows
print("📄 First 5 Rows:\n", df.head())

# Show column names
print("\n📦 Columns:", df.columns.tolist())

# Basic info
print("\n🔍 Data Info:")
print(df.info())

# Check for null values
print("\n⚠️ Missing values:\n", df.isnull().sum())

# Drop rows with missing values in key columns
df = df.dropna(subset=["date_added", "duration", "rating"])

# ✅ Fix: Strip leading/trailing spaces in 'date_added' & safely convert to datetime
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')

# Extract year and month from the cleaned date
df['added_year'] = df['date_added'].dt.year
df['added_month'] = df['date_added'].dt.month

# Final cleaned info
print("\n✅ Cleaned dataset info:")
print(df.info())

# Set seaborn style
sns.set(style="whitegrid")

# 📊 Chart 1: Countplot - Titles Added Per Year
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='added_year', order=sorted(df['added_year'].dropna().unique()), palette='viridis')
plt.title("📅 Number of Titles Added to Netflix Each Year", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
# plt.savefig("charts/netflix_yearly_additions.png")
plt.show()

# 📊 Chart 2: Pie Chart - TV Shows vs Movies
type_counts = df['type'].value_counts()
plt.figure(figsize=(6,6))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title("📺 Distribution of Movies vs TV Shows on Netflix")
plt.axis('equal')
plt.tight_layout()
# plt.savefig("charts/netflix_type_distribution.png")
plt.show()

# 📊 Chart 3: Top 10 Genres
df_genres = df.dropna(subset=["listed_in"])
all_genres = []
for entry in df_genres['listed_in']:
    genres = [g.strip() for g in entry.split(',')]
    all_genres.extend(genres)
genre_counts = Counter(all_genres)
top_genres = genre_counts.most_common(10)
genres, counts = zip(*top_genres)
plt.figure(figsize=(10,6))
sns.barplot(x=list(counts), y=list(genres), palette="magma")
plt.title("🎭 Top 10 Genres on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
plt.tight_layout()
# plt.savefig("charts/top_genres_netflix.png")
plt.show()

# 📊 Chart 4: Top 10 Countries
df_countries = df.dropna(subset=["country"])
top_countries = df_countries['country'].value_counts().head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette="crest")
plt.title("🌍 Top 10 Countries by Number of Netflix Titles")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
plt.tight_layout()
# plt.savefig("charts/top_countries_netflix.png")
plt.show()

# Separate Movies and TV Shows
movies = df[df['type'] == 'Movie']
tv_shows = df[df['type'] == 'TV Show']

# Clean and extract numeric duration
# Movies: extract minutes
movies['duration_min'] = movies['duration'].str.extract('(\d+)').astype(float)

# TV Shows: extract season counts
tv_shows['seasons'] = tv_shows['duration'].str.extract('(\d+)').astype(int)

# Plot both side by side
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Movie Duration Distribution
sns.histplot(movies['duration_min'].dropna(), bins=30, kde=True, ax=axes[0], color='skyblue')
axes[0].set_title("⏱️ Movie Duration (in Minutes)")
axes[0].set_xlabel("Duration (minutes)")
axes[0].set_ylabel("Count")

# Right: TV Show Season Count
sns.countplot(x=tv_shows['seasons'], palette='light:#5A9', ax=axes[1])
axes[1].set_title("📺 Number of Seasons in TV Shows")
axes[1].set_xlabel("Number of Seasons")
axes[1].set_ylabel("Count")
axes[1].set_xticks(range(1, tv_shows['seasons'].max() + 1))

plt.tight_layout()
# plt.savefig("charts/duration_analysis.png")
plt.show()

# Top 10 Actors
actor_list = df['cast'].dropna().str.split(', ')
all_actors = [actor for sublist in actor_list for actor in sublist]
actor_counts = Counter(all_actors)
top_actors = actor_counts.most_common(10)
actors, actor_freqs = zip(*top_actors)

# Top 10 Directors
director_list = df['director'].dropna().str.split(', ')
all_directors = [d for sublist in director_list for d in sublist]
director_counts = Counter(all_directors)
top_directors = director_counts.most_common(10)
directors, director_freqs = zip(*top_directors)

# Plot side-by-side
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left: Top Actors
sns.barplot(x=list(actor_freqs), y=list(actors), palette="rocket", ax=axes[0])
axes[0].set_title("🎬 Top 10 Actors on Netflix")
axes[0].set_xlabel("Number of Appearances")
axes[0].set_ylabel("Actor")

# Right: Top Directors
sns.barplot(x=list(director_freqs), y=list(directors), palette="flare", ax=axes[1])
axes[1].set_title("🎥 Top 10 Directors on Netflix")
axes[1].set_xlabel("Number of Appearances")
axes[1].set_ylabel("Director")

plt.tight_layout()
# plt.savefig("charts/top_actors_directors.png")
plt.show()
