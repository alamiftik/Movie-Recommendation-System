import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests


# streamlit run app.py


# User defined function to fetch movies poster from TMDB website.
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=0d78280c3c1d71310cc016b2893c6bf6&language-en-US".format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']


# Function will do the following actions
# 1) - Function to find index number of the selected movie name.
# 2) - Function will find the angle distance between selected movie to other movies.
# 3) - Function will perform descending order of angular distance.

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(similarity[0])), reverse=True, key = lambda x:x[1])[1:6]

# For loop will check and propose suggested similar movies to the user
    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append((movies.iloc[i[0]].title))
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# opened 'movie_dict.pkl' and 'similarity.pkl' files and saved as DataFream in variables.
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

# Add Title of the website.
st.title("Movie Recommendation System")

# add selection box and include list of movies for the selection.
selected_movie_name = st.selectbox("Enter the name of the movie", movies['title'].values)


# Add button on the website & it will show the closest 5 movies to user
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

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
