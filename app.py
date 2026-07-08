import streamlit as st
import pickle
import pandas as pd
import requests



background_posters = [
    "https://image.tmdb.org/t/p/w500/gKY6q7SjCkAU6FqvqWybDYgUKIF.jpg",
    "https://image.tmdb.org/t/p/w500/jGWpG4YhpQwVmjyHEGkxEkeRf0S.jpg",
    "https://image.tmdb.org/t/p/w500/zj8ongFhtWNsVlfjOGo8pSr7PQg.jpg",
    "https://image.tmdb.org/t/p/w500/hr0L2aueqlP2BYUblTTjmtn0hw4.jpg",
    "https://image.tmdb.org/t/p/w500/lCxz1Yus07QCQQCb6I0Dr3Lmqpx.jpg",
    "https://image.tmdb.org/t/p/w500/qFmwhVUoUSXjkKRmca5yGDEXBIj.jpg",
    "https://image.tmdb.org/t/p/w500/ym7Kst6a4uodryxqbGOxmewF235.jpg",
    "https://image.tmdb.org/t/p/w500/4ssDuvEDkSArWEdyBl2X5EHvYKU.jpg",
    "https://image.tmdb.org/t/p/w500/z7uo9zmQdQwU5ZJHFpv2Upl30i1.jpg",
    "https://image.tmdb.org/t/p/w500/5UsK3grJvtQrtzEgqNlDljJW96w.jpg",
    "https://image.tmdb.org/t/p/w500/385XwTQZDpRX2d3kxtnpiLrjBXw.jpg",
    "https://image.tmdb.org/t/p/w500/e3DXXLJHGqMx9yYpXsql1XNljmM.jpg",
]






st.set_page_config(page_title="Movie Recommender", layout="centered")

st.markdown("""
    <style>
            
    body, p, span, label, div {
        color: white !important;
    }

    html, body {
        height: 100%;
    }
    
    .stApp {
        background-color: transparent !important;
    }
    .poster-background {
        position: fixed !important;
        inset: 0;
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 0px !important;
        z-index: -1 !important;
        filter: blur(2px) brightness(0.25) !important;
        overflow: hidden;
        background-color: #000000;
    }
    .poster-background img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .main-title {
        color: #ff3b3b;
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        color: #b3b3b3;
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
    }
            

    /* Dropdown outer container */
    .react-aria-ComboBox {
        background-color: #1a1a1a !important;
        border-radius: 8px !important;
    }
    /* Dropdown input box + text */
    .react-aria-ComboBox input[role="combobox"] {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #ffffff !important;
        border-radius: 8px !important;
    }
    /* The little dropdown arrow button */
    .react-aria-ComboBox button {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    /* The open dropdown list */
    div[role="listbox"] {
        background-color: #1a1a1a !important;
    }
    div[role="listbox"] * {
        background-color: #1a1a1a !important;
        color: white !important;
    }
            
    /* Selectbox label text */
    .stSelectbox label {
        color: white !important;
    }
    .stSelectbox label p {
        color: white !important;
    }
            
    
            
    button:has(div[data-testid="stMarkdownContainer"]) {
        background: linear-gradient(90deg, #ff3b3b, #ff1a4f) !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        box-shadow: 0 0 15px rgba(255, 59, 59, 0.5) !important;
    }
    button:has(div[data-testid="stMarkdownContainer"]):hover {
        box-shadow: 0 0 25px rgba(255, 59, 59, 0.8) !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: white !important;
    }
            
    /* Movie name labels under posters */
    div[data-testid="stText"] {
        color: white !important;
    }


    .block-container {
        background-color: rgba(20, 20, 20, 0.92) !important;
        border-radius: 20px !important;
        padding: 50px 60px !important;
        max-width: 900px !important;
        margin: 60px auto !important;
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.6) !important;
    } 

    </style>
""", unsafe_allow_html=True)



def get_background_html():
    posters_html = "".join([f'<img src="{url}">' for url in background_posters * 3])
    return f"""
    <div class="poster-background">
        {posters_html}
    </div>
    """

st.markdown(get_background_html(), unsafe_allow_html=True)



st.markdown('<div class="main-title">🎬 MOVIE RECOMMENDER SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover movies similar to your favorites using content-based machine learning</div>', unsafe_allow_html=True)




@st.cache_resource
def load_data():
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()



@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={st.secrets['tmdb']['api_key']}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_titles = []
    recommended_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_titles, recommended_posters







# Dropdown of all movie titles
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select a movie to get recommendations:",
    movie_list
)




if st.button('Recommend Similar Movies'):
    with st.spinner('Finding similar movies...'):
        names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])