'''Many broad approaches were brainstormed with Sophia Hager. Python for Data Analysis Chapter 8, the Pandas and Numpy documentation, and cited Googled sources have been crucial to the data wrangling in this project. Any borrowed syntax/code is commented above the code.'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_data():
    '''read in data from archive folder and return'''
    # read in data
    # from https://www.kaggle.com/bahramjannesarr/goodreads-book-datasets-10m
    books1 = pd.read_csv("./archive/user_rating_0_to_1000.csv")
    books2 = pd.read_csv("./archive/user_rating_1000_to_2000.csv")
    books = pd.concat([books1, books2])
    
    return books

def clean_data(books, nbook_ratings = 20, nuser_ratings = 5):
    '''take book rating data, return users x books w/ rating values as numpy array'''
    # https://www.programiz.com/python-programming/function-argument
    
    # filter out no ratings
    books = books[books['Rating'] != "This user doesn't have any rating"]
    
    # ratings to numeric from
    # https://datatofish.com/replace-values-pandas-dataframe/
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.replace.html
    books = books.replace(['it was amazing', 'really liked it', 'liked it', 'it was ok', 'did not like it'],
                          [5, 4, 3, 2, 1])

    # pivot observations = users
    # from PyDA chapter 8
    users = books.pivot('ID', 'Name', 'Rating')

    # remove books w/ fewer than nbook_ratings ratings
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.count.html
    # https://stackoverflow.com/questions/29281815/pandas-select-dataframe-columns-using-boolean
    users = users.loc[:, users.count() > nbook_ratings]

    # remove users who have rated fewer than nuser_ratings of these
    users = users[(users.count(axis = 1) > nuser_ratings)]

    # to numpy
    # thanks to Sophia for the dtype
    users_np = users.to_numpy(dtype = 'float')
    
    # replace nan with 0
    # https://numpy.org/doc/stable/reference/generated/numpy.nan_to_num.html
    users_np = np.nan_to_num(users_np)
    
    # also return book names as list
    book_names = users.columns
    
    return users_np, book_names

def predict(users_np, n = 5):
    '''return predictions using n dimensions of SVD'''    
    # SVD
    U_small,S_small,V_small = np.linalg.svd(users_np,full_matrices=False)
    users_svd = U_small[:, :n] * S_small[:n]

    # return to original dimensions
    users_predictions = np.dot(users_svd, V_small[:n])
    
    # translate to original ratings
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.round_.html
    users_predictions = np.round(users_predictions)
    users_predictions[users_predictions <= 0] = 0
    users_predictions[users_predictions > 5] = 5
    
    return users_predictions

def make_recommendations(users, predictions, book_names):
    '''given user ratings and predicted ratings, recommend un-rated books'''
    # remove predictions where already rated in original
    # https://stackoverflow.com/questions/6701714/numpy-replace-a-number-with-nan
    predictions[users != 0] = np.nan

    # to pandas
    predictions_pd = pd.DataFrame(predictions, columns = book_names)
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html
    predictions_pd = predictions_pd.reset_index()
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
    predictions_pd = predictions_pd.rename(columns={"index": "User"})

    # trying to get 3 recommendations for all users
    
    # one rating per row
    # PyDA ch. 8
    # https://pandas.pydata.org/docs/reference/api/pandas.melt.html
    predictions_long = pd.melt(predictions_pd, id_vars = ["User"], value_name='Rating', ignore_index = False)

    # sort for top recommendations
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html
    predictions_long = predictions_long.sort_values('Rating', ascending = False)

    # take top 3 recommendations for each user
    # https://stackoverflow.com/questions/20069009/pandas-get-topmost-n-records-within-each-group
    predictions_long = predictions_long.groupby('User').head(3)

    # sort by user
    predictions_long = predictions_long.sort_values('User')
    
    # don't recommend already rated (NaN) or 0-rated
    # https://datatofish.com/check-nan-pandas-dataframe/
    # https://www.geeksforgeeks.org/python-pandas-dataframe-notnull/
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.where.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.copy.html
    predictions_copy = predictions_long.copy()
    m = predictions_copy['Rating'] != 0 & predictions_copy['Rating'].notnull()
    predictions_copy['Name'] = predictions_copy['Name'].where(m, 'None')
    predictions_copy['Rating'] = predictions_copy['Rating'].where(m, 'N/A')
    
    # one recommendation per user
    # https://numpy.org/doc/stable/reference/generated/numpy.reshape.html
    recommend = np.reshape(predictions_copy.to_numpy(), (predictions_copy.shape[0]//3, 9))
    
    recommendations = pd.DataFrame(recommend, columns = ['User', 'Book 1', 'Rating 1',
                                                        'User_2', 'Book 2', 'Rating 2',
                                                        'User_3', 'Book 3', 'Rating 3'])
    
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html
    recommendations = recommendations.drop(columns=['User_2', 'User_3'])
    
    return recommendations 
    
def recommender():
    '''Run entire recommender process'''
    books = get_data()
    users_np, book_names = clean_data(books, nbook_ratings = 20, nuser_ratings = 5)
    predictions = predict(users_np)
    recommendations = make_recommendations(users_np, predictions, book_names)
    # also return user ratings in pandas df for comparison
    users = pd.DataFrame(users_np, columns = book_names)
    return recommendations, users

recommendations, users = recommender()

# for examining specifc user's ratings
def get_user_ratings(user_num):
    '''return dataframe of titles a specific user has rated'''
    # relies on users existing as a global variable
    # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#selection-by-position
    user = users.iloc[user_num:user_num+1, :]

    # take only columns w/ recommendations
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.dropna.html
    user = user[user > 0].dropna(axis = 1)

    # column of titles, column of ratings
    user_long = pd.melt(user, var_name = 'Book', value_name='Rating')
    
    return user_long

# for examining specifc user's recommendation
def get_user_recommendations(user_num):
    '''return dataframe of recommendations for a specific user'''
    # relies on recommendations existing as a global variable
    recs = recommendations.iloc[user_num:user_num+1, :]
    
    return recs
