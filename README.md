# Movie Recommender System

A content-based movie recommendation system built with Python and Streamlit. Select a movie and get 5 similar recommendations with posters, powered by cosine similarity on movie metadata (genres, cast, crew, keywords) from a TMDB 5000 movie dataset.

## Tech Stack
- Python, pandas, scikit-learn (model)
- Streamlit (frontend/deployment)
- TMDB API (poster fetching)

## How it works
Movie metadata is vectorized and compared using cosine similarity, precomputed offline into a similarity matrix. At runtime, the app looks up the selected movie's precomputed similarity scores, ranks them, fetches poster images for the top 5 matches via the TMDB API, and renders everything in a custom dark-themed UI.

## Live Demo
