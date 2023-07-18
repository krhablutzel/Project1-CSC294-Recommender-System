import pytest
import pandas as pd
import numpy as np
import project1

# surface level tests
def test_users_type():
    assert isinstance(project1.users, pd.DataFrame)

def test_recommendations_type():
    assert isinstance(project1.recommendations, pd.DataFrame)
    
def test_recommendations_size():
    expected = (project1.users.shape[0], 7)
    assert project1.recommendations.shape == expected
    
# no repeat recommendations
def test_recommendations_unique():
    # for each user
    for i in range(project1.users.shape[0]):
        # get lists of rated books and recommended books
        recs = project1.get_user_recommendations(i)
        recs_list = recs['Book 1'].tolist() + recs['Book 2'].tolist() + recs['Book 3'].tolist()
        rates_list = project1.get_user_ratings(i)['Book'].tolist()

        # convert to sets, assert no common elements
        recs_set = set(recs_list)
        rates_set = set(rates_list)
        assert len(recs_set & rates_set) == 0
    
