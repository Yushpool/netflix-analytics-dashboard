import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Page settings
st.set_page_config(page_title="Netflix Analytics", layout="wide")
st.title("🎬 Netflix Titles Data Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df = df.dropna(subset=["date_added", "duration", "rating"])
    df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')
    df['added_year'] = df['date_added'].dt.year
    df['added_month'] = df['date_added'].dt.month
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("📊 Filter the Data")

# Year range slider
year_range = st.sidebar.slider("Select Year Range", int(df['added_year'].min()), int(df['added_year'].max()), (2015, 2021))

# Dropdown filters
type_filter = st.sidebar.selectbox("Select Type", options=["All"] + sorted(df['type'].dropna().unique().tolist()))
country_filter = st.sidebar.selectbox("Select Country", options=["All"] + sorted(df['country'].dropna().unique()))
genre_filter = st.sidebar.selectbox("Select Genre", options=["All"] + sorted(set(g.strip() for sub in df['listed_in'].dropna() for g in sub.split(','))))

# Apply filters
filtered_df = df.copy()
if type_filter != "All":
    filtered_df = filtered_df[filtered_df['type'] == type_filter]
if country_filter != "All":
    filtered_df = filtered_df[filtered_df['country'].str.contains(country_filter, na=False)]
if genre_filter != "All":
    filtered_df = filtered_df[filtered_df['listed_in'].str.contains(genre_filter, na=False)]
filtered_df = filtered_df[filtered_df['added_year'].between(year_range[0], year_range[1])]

# Tabs for better UI
tab1, tab2, tab3, tab4 = st.tabs(["📅 Yearly Trend", "📺 Type Ratio", "🎭 Genres", "🌍 Countries"])

# 1. Yearly Trend
with tab1:
    st.subheader("📅 Titles Added Per Year")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.countplot(data=filtered_df, x='added_year', order=sorted(filtered_df['added_year'].dropna().unique()), palette='viridis', ax=ax1)
    ax1.set_title("Titles Added by Year")
    st.pyplot(fig1)

# 2. Movie vs TV Show
with tab2:
    st.subheader("📺 Movies vs TV Shows")
    type_counts = filtered_df['type'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
    ax2.axis('equal')
    st.pyplot(fig2)

# 3. Top Genres
with tab3:
    st.subheader("🎭 Top Genres")
    all_genres = []
    for entry in filtered_df['listed_in'].dropna():
        genres = [g.strip() for g in entry.split(',')]
        all_genres.extend(genres)
    genre_counts = Counter(all_genres)
    top_genres = genre_counts.most_common(10)
    genres, counts = zip(*top_genres)
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=list(counts), y=list(genres), palette="magma", ax=ax3)
    st.pyplot(fig3)

# 4. Top Countries
with tab4:
    st.subheader("🌍 Top Countries by Content")
    top_countries = filtered_df['country'].dropna().value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="crest", ax=ax4)
    st.pyplot(fig4)
