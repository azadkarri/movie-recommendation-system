import streamlit as st
import pickle
import pandas as pd
import base64


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movies_list:
        title = movies.iloc[i[0]]['title']
        rating = movies.iloc[i[0]]['vote_average']

        recommended_movies.append((title, rating))

    return recommended_movies


# Load Data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def get_base64(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_image = get_base64("mov.jpg")

st.markdown(f"""
<style>

.stApp {{
    background:
    linear-gradient(
        rgba(0,0,0,0.110),
        rgba(0,0,0,0.100)
    ),
    url("data:image/jpg;base64,{bg_image}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

h1 {{
    color: #FFD700 !important;
    text-align: center;
}}

h2, h3 {{
    color: white !important;
}}

p {{
    color: #ff1493 !important;
    font-weight: bold;
}}

.stButton > button,
.stButton > button * {{
    background-color: red !important;
    color: white !important;
}}

.stSelectbox label {{
    color: white !important;
    font-size: 18px;
}}

.stSelectbox label {{
    color: #ff1493 !important;
    font-size: 18px;
    font-weight: bold;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 15px;
    border: 2px solid #ff1493;
    border-radius: 30px;
    background: rgba(0,0,0,0.5);
}}

</style>
""", unsafe_allow_html=True)
st.title("🎬 Intelligent Movie Recommendation System")
st.markdown("---")

st.markdown("""
<div style="
background: rgba(0,0,0,0.75);
padding: 40px;
border-radius: 25px;
text-align: center;
border: 1px solid rgba(255,215,0,0.5);
box-shadow: 0px 0px 30px rgba(255,215,0,0.25);
backdrop-filter: blur(12px);
">

<div style="
display:inline-block;
background: linear-gradient(90deg,#FFD700,#FFA500);
color:black;
padding:8px 20px;
border-radius:30px;
font-weight:bold;
font-size:14px;
letter-spacing:1px;
margin-bottom:20px;
">
FINAL YEAR PROJECT 2026
</div>

<h1 style="
color:#FFD700;
font-size:48px;
margin:0;
font-weight:800;
letter-spacing:1px;
">
🎬 Movie Recommendation System
</h1>

<h3 style="
color:white;
margin-top:15px;
font-weight:400;
">
Content-Based Movie Recommendation using NLP & Machine Learning
</h3>

<p style="
color:white;
font-size:18px;
margin-top:15px;
">
AI-powered movie recommendations based on content similarity.
</p>

<div style="
margin-top:25px;
display:flex;
justify-content:center;
gap:25px;
flex-wrap:wrap;
">


<div style="margin-top:12px;">
    <a href="https://www.google.com/search?q=movie+list"
    target="_blank"
    style="
        background:rgba(255,255,255,0.08);
padding:12px 25px;
border-radius:15px;
color:white;
    ">
        🎬 Thousands of Movies Available →
    </a>
</div>

<a href="https://www.kaggle.com/datasets"
target="_blank"
style="
background:rgba(255,255,255,0.08);
padding:12px 25px;
border-radius:15px;
color:white;
text-decoration:none;
display:inline-block;
">
📂 DataSets
</a>

<a href="https://www.google.com/search?q=Hollywood+all+time+blockbuster+movies"
target="_blank"
style="
background:rgba(255,255,255,0.08);
padding:12px 25px;
border-radius:15px;
color:white;
text-decoration:none;
display:inline-block;
">
⭐ Smart Recommendations
</a>

</div>
""", unsafe_allow_html=True)


st.markdown("---")

col1, col2 = st.columns([3,1])

with col2:
    search_type = st.selectbox(
        "Category",
        ["Director", "Hero", "Heroine", "Actor"]
    )

    search_name = st.text_input("Search Name")

    if search_name:
        google_url = f"https://www.google.com/search?q={search_name.replace(' ', '+')}+movies"
        st.link_button("🔍 Search", google_url)

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies['title'].values
)
st.markdown("""
<style>
.stButton > button {
    background: red !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
if st.button("Recommend"):

    # Selected movie rating
    selected_movie = movies[movies['title'] == selected_movie_name].iloc[0]
    selected_rating = selected_movie['vote_average']

    st.markdown("""
    <div style="
        display: inline-block;
        background: rgba(0,0,0,0.6);
        padding: 10px 25px;
        border-radius: 50px;
        border: 2px solid #ff1493;
        box-shadow: 0px 0px 12px rgba(255,20,147,0.3);
        margin-bottom: 10px;
    ">
        <h3 style="color:white; margin:0;">🎬 Selected Movie</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
        padding: 15px 25px;
        border-radius: 50px;
        margin-bottom: 15px;
        border: 2px solid #ff1493;
        box-shadow: 0px 0px 18px rgba(255,20,147,0.4);
    ">
        🎥 <span style="color:white; font-weight:bold;">{selected_movie_name}</span>
        &nbsp; | &nbsp;
        ⭐ <span style="color:#FFD700;">{selected_rating / 2:.1f}/5</span>
        &nbsp; | &nbsp;
        📊 <span style="color:#ff1493;">{selected_rating:.1f}/10</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    recommendations = recommend(selected_movie_name)

    st.markdown("""
    <div style="
        display: inline-block;
        background: rgba(0,0,0,0.6);
        padding: 10px 25px;
        border-radius: 50px;
        border: 2px solid #FFD700;
        box-shadow: 0px 0px 12px rgba(255,215,0,0.3);
        margin-bottom: 10px;
    ">
        <h3 style="color:white; margin:0;">🎯 Top 5 Recommended Movies</h3>
    </div>
    """, unsafe_allow_html=True)

    for movie, rating in recommendations:
        google_link = f"https://www.google.com/search?q={movie.replace(' ', '+')}"

        st.markdown(f"""
        <div style="
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
            padding: 12px 20px;
            border-radius: 50px;
            margin-bottom: 10px;
            border: 2px solid #FFD700;
            box-shadow: 0px 0px 15px rgba(255,215,0,0.3);
        ">
            🎬 <a href="{google_link}" target="_blank"
            style="color:white; font-weight:bold; text-decoration:none;">
            {movie}
            </a>
            &nbsp; | &nbsp;
            ⭐ <span style="color:#FFD700;">{rating / 2:.1f}/5</span>
            &nbsp; | &nbsp;
            📊 <span style="color:#ff1493;">{rating:.1f}/10</span>
        </div>
        """, unsafe_allow_html=True)