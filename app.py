import streamlit as st
import pickle
import pandas as pd
import joblib
import requests

# Load Data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = joblib.load(open('similarity.pkl', 'rb'))

# Function to fetch movie poster from API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster+Found"
    except Exception as e:
        print("Poster fetch error for movie_id", movie_id, ":", e)
        return "https://via.placeholder.com/500x750.png?text=Image+Not+Available"

# Recommendation Logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster_url = fetch_poster(movie_id)

        if poster_url:  # Only add if valid poster
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(poster_url)

        if len(recommended_movies) == 5:
            break

    return recommended_movies, recommended_movies_posters


# Page Config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        background: -webkit-linear-gradient(left, #FF416C, #FF4B2B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .movie-title {
        font-size: 16px;
        font-weight: 600;
        text-align: center;
        margin-top: 10px;
        color: #FF4B2B;
    }
    .stSelectbox label {
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown('<div class="main-title">🎬 Movie Recommender System</div>', unsafe_allow_html=True)

# Movie Selection
selected_movie_name = st.selectbox('Choose a movie to get similar recommendations:', movies['title'].values)

# Recommend Button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i]:
            st.image(posters[i], use_column_width=True)
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)
