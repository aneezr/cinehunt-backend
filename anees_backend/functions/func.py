import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split

filename_movies = "static\movies.csv"
filename_ratings = r"D:\Btech\Project\anees_backend\anees_backend\static\ratings.csv"


def genre_recommendations(title,count):
    movies = pd.read_csv(filename_movies)
    # Break up the big genre string into a string array
    moviesforcontent = movies.copy()
    moviesforcontent['genres'] = moviesforcontent['genres'].str.split('|')
    # Convert genres to string value
    moviesforcontent['genres'] = moviesforcontent['genres'].fillna("").astype('str')

    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(moviesforcontent['genres'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    titles = movies['title']
    indices = pd.Series(movies.index, index=movies['title'])
    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    
    return titles.iloc[movie_indices].iloc[count]

def CF_func(userMovieIds,userMovieRates,num):
    ratings = pd.read_csv(filename_ratings)
    ratings.drop(['timestamp'], axis=1, inplace=True)
    movies = pd.read_csv(filename_movies)

    #add to dataset
    #userMovieIds = [4,166534,1]
    #userMovieRates = [5,1,3]
    userId = [611] * len(userMovieIds)
    dict = {'userId': userId,
            'movieId':userMovieIds,
            'rating':userMovieRates
        }
    
    df = pd.DataFrame(dict)
    rates = pd.concat([ratings, df], ignore_index = True)

    X_train, X_test = train_test_split(rates, test_size = 0.30, random_state = 42)

    dummy_train = X_train.copy()
    dummy_test = X_test.copy()
    
    user_data = X_train.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(0)

    # The movies not rated by user is marked as 1 for prediction 
    dummy_train = dummy_train.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(1)

    # The movies not rated by user is marked as 0 for evaluation 
    dummy_test = dummy_test.pivot(index ='userId', columns = 'movieId', values = 'rating').fillna(0)


    # User Similarity Matrix using Cosine similarity as a similarity measure between Users
    user_similarity = cosine_similarity(user_data)
    user_similarity[np.isnan(user_similarity)] = 0

    user_predicted_ratings = np.dot(user_similarity, user_data)

    user_final_ratings = np.multiply(user_predicted_ratings, dummy_train)

    cf_output = user_final_ratings.iloc[610].sort_values(ascending = False)[0:num]

    return cf_output