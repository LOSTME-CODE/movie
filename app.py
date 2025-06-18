import streamlit as st
import pickle
import pandas as pd
import requests

# CSS Styling for better layout and image size
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        [data-testid="stAppViewContainer"] {
            background-color: black;
            text-align: center;
        }  
        [data-testid="stSidebar"] {
            background-color: #1e1e1e;
        }
        .stTextInput, .stSelectbox label {
            color: white !important;
        }

        .stButton>button {
            background-color: black !important;
            color: white !important;
            border-radius: 10px;
            border: 1px solid white;
            padding: 10px 20px;
            font-weight: bold;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #222 !important;
            color: white !important;
        }

        .title {
            color: white !important;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
        }

        label[data-testid="stWidgetLabel"] {
            color: white !important;
            font-size: 18px;
            font-weight: bold;
        }

        .poster-img img {
            height: 300px !important;
            width: auto !important;
            display: block;
            margin: auto;
            border-radius: 10px;
            border: 2px solid white;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# Function to fetch movie posters
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get("poster_path", "")
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/200x300?text=No+Image"

# Movie recommendation function
def recommend(movie):
    try:
        movie_index = movies[movies["title"] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(
            list(enumerate(distances)), reverse=True, key=lambda x: x[1]
        )[1:6]

        recommended_movies = []
        recommended_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_posters
    except IndexError:
        return [], []

# Load movie data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open("similarity.pkl", "rb"))

# Debug: Show similarity object type and shape
st.write("🔍 Similarity type:", type(similarity))
st.write("🧩 Similarity shape:", getattr(similarity, 'shape', 'N/A'))

# Convert to numpy array if needed
if isinstance(similarity, pd.DataFrame):
    similarity = similarity.to_numpy()
    st.write("🔁 Converted similarity to numpy array.")

# Initialize session state for image visibility
if "show_poster" not in st.session_state:
    st.session_state.show_poster = True

# UI Title
st.markdown('<p class="title">🎬 Movie Recommender System</p>', unsafe_allow_html=True)

# Dropdown for selecting a movie
selected_movie_name = st.selectbox("Select a movie to get recommendations:", movies["title"].values)

# Button to trigger recommendations
if st.button("Recommend"):
    st.session_state.show_poster = False  # Hide default poster

    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(5)  # Create 5 columns dynamically
        for i, col in enumerate(cols):
            with col:
                st.text(names[i])
                st.image(posters[i], use_column_width=True)
    else:
        st.warning("No recommendations found. Try another movie.")

# Show default poster if nothing is recommended
if st.session_state.show_poster:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("poster.jpg", caption="Default Poster", width=300)
        except Exception as e:
            st.warning("Poster image not found.")
            st.text(str(e))
