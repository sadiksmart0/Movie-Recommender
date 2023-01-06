
import pandas as pd
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

##############   LOADING DATA  ###################################
movie_df = pd.read_csv("../Movie_Recomender/ml-25m/Allmovie.csv")
ratings = pd.read_csv("../Movie_Recomender/ml-25m/ratings.csv")

#Declare Vecorizer
vectorizer = TfidfVectorizer(ngram_range=(1,2))

##################  CLEANING TITLE ################################
def clean_data(title):
    return re.sub("[^a-zA-Z0-9 ]", "", title)

#apply clean data to all titles
movie_df["clean_title"] = movie_df["title"].apply(clean_data)

################### VECTORIZE SEARCH PARAMETERS #####################
def vectorize_search(title):
    title = clean_data(title)
    tfidf_all = vectorizer.fit_transform(movie_df["clean_title"])
    title_vec = vectorizer.transform([title])
    results = get_similar(title_vec, tfidf_all)
    return results

#####################  GET SIMILAR MOVIES BASED ON COSINE SIMILARITY  ###################
def get_similar(title_vec, tfidf_all_vec):
    similarity = cosine_similarity(title_vec, tfidf_all_vec).flatten()
    indices = np.argpartition(similarity, -1)[-1:]
    results = movie_df.iloc[indices]
    return results

###################   RECOMMMEND MOVIES   ###############################################
def recommend(movie_id):
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
    
    return rec_per.head(10).merge(movie_df, left_index=True, right_on="movieId")[["movieId","title","genres","tmdbId"]]

