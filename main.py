
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("../Movie_Recomender/ml-25m/Allmovie.csv")
ratings = pd.read_csv("../Movie_Recomender/ml-25m/ratings.csv")

def clean_data(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

df["clean_title"] = df["title"].apply(clean_data)
vectorizer = TfidfVectorizer(ngram_range=(1,2))
tfidf = vectorizer.fit_transform(df["title"])

def search(title):
    title = clean_data(title)
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -1)[-1:]
    results = df.iloc[indices]
    return results


def similar(movie_id):
    sim_users = ratings[(ratings["movieId"] == int(movie_id)) & (ratings["rating"]>= 4)]["userId"].unique()
    sim_users_recs = ratings[(ratings["userId"].isin(sim_users)) & (ratings["rating"]> 4)]["movieId"]
    
    sim_users_recs = sim_users_recs.value_counts() / len(sim_users)
    sim_users_recs = sim_users_recs[sim_users_recs > .1]

    all_users = ratings[(ratings["movieId"].isin(sim_users_recs.index)) & (ratings["rating"] > 4)]
    all_users_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
    
    rec_per = pd.concat([sim_users_recs, all_users_recs], axis=1)
    rec_per.columns = ["similar","all"]
    
    rec_per["score"] = rec_per["similar"] / rec_per["all"]
    rec_per = rec_per.sort_values("score", ascending=False)
    
    return rec_per.head(10).merge(df, left_index=True, right_on="movieId")[["movieId","title","genres","tmdbId"]]

