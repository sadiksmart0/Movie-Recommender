import streamlit as st
from main import search, similar
from PIL import Image
from web_scraping import get_movie_data

st.title("BlockBusters THRILLER Movies")
img1 = Image.open("C:/Users/A.M. MUKTAR/Movie_Recomender/MOVIETIME.jpg")
st.image(img1,use_column_width=True)

tab1, tab2 = st.tabs(["Home", "Explore  All"])

with tab1:
    st.header("Search and Get Recommendations")
    title = st.text_input("Enter Movie Title")
    if st.button('Search'):
        result1 = search(title)
        result2 = similar(result1["movieId"])
        scrape = get_movie_data(result2)
        # Iterate through each movie in the input dataframe
        for index, row in scrape.iterrows():
            st.header(row["title"])
            st.image(row["poster_url"], use_column_width='auto')
            st.write(f'Ratings: {row["rating"]}')
            st.write(row["description"])
            mid = f'https://movielens.org/movies/{row["movieId"]}'
            st.write("[Watch Movie]({})".format(mid))
                
    else:
        st.write('Goodbye')


with tab2:
    st.header("Latest BlockBusters")
