import pandas as pd
import requests
from bs4 import BeautifulSoup


root = 'https://www.themoviedb.org'

def get_movie_data(movies_df):
    movie_data = []
    
    # Iterate through each movie in the input dataframe
    for index, row in movies_df.iterrows():
        imdb_id = row['tmdbId']
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        # Make a request to the IMDb calendar page for the movie
        response = requests.get(f'https://www.themoviedb.org/movie/{imdb_id}', headers=headers)
        
        # Parse the HTML of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the movie poster image URL
        poster_img_tag = soup.find('img', class_='poster')
        poster_img_url = poster_img_tag['src'] if poster_img_tag else None
        
        # Find the movie title and description
        title_tag = soup.find('h2', class_='9')
        title = title_tag.text.strip() if title_tag else row['title']
        description_tag = soup.find('div', class_='overview')
        description = description_tag.text.strip() if description_tag else None
        
        # Find the movie rating
        rating_tag = soup.find('div', class_='false')
        rating = rating_tag.text.strip() if rating_tag else None
        
        # Add the scraped data to the list
        movie_data.append({
            'title': title,
            'description': description,
            'poster_url': root+poster_img_url,
            'rating': rating,
            'tmdbId': row['tmdbId'],
            'movieId': row['movieId']
        })
    
    # Return the list of movie data as a new dataframe
    return pd.DataFrame(movie_data)
