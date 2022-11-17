"""
Mateusz Miekicki s20691
Oskar Przydatek s19388
Selection of which films a user should watch and 
which they should not on the basis of their and other users' film ratings.
"""

import json
import numpy as np


def euclidean_score(dataset: json, user1: str, user2: str):
    '''
     Function checking similarity of users movies using euclidean distance
    Parameters:
    dataset (json): dataset in json format
    user1 (str): first user
    user2 (str): second user
    Returns:
    score: Similarity of the selected films 
    '''
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(
                np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


def pearson_score(dataset: json, user1: str, user2: str):
    '''
    Function checking similarity of users movies using pearson correlation
    Parameters:
    dataset (json): dataset in json format
    user1 (str): first user
    user2 (str): second user
    Returns:
    score: Similarity of the selected films 
    '''
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}
    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    num_ratings = len(common_movies)
    if num_ratings == 0:
        return 0
    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    user1_squared_sum = np.sum(
        [np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum(
        [np.square(dataset[user2][item]) for item in common_movies])

    sum_of_products = np.sum(
        [dataset[user1][item] * dataset[user2][item] for item in common_movies])

    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


class RecommendationSystem:
    def __init__(self, data, user):
        self.users_and_scores = {}
        self.most_compatible_users = []
        self.data = data
        self.user = user

    def get_nearest_user(self, user_to_compare):
        '''
        Function getting the most similar user to compared one.
        Parameters:
        user_to_compare (str): user to compare
        Returns:
        user: nearest user
        '''
        user_list = list(self.data.keys())
        user_list.remove(user_to_compare)
        highest_score = 0
        for u in user_list:
            score = pearson_score(data, user_to_compare, u)
            # euclidean_score(data, user_to_compare, u)
            self.users_and_scores[u] = score
            if score >= highest_score:
                highest_score = score
                nearest_user = u
        return nearest_user

    def get_nearest_users_list(self, user_to_compare):
        '''
        Function getting list of most similar users to compared one.
        Parameters:
        user_to_compare (str): user to compare
        Returns:
        user: nearest user list
        '''
        nearest = self.get_nearest_user(user_to_compare)
        sorted_nearest_users_dict = {k: v for k, v in sorted(
            self.users_and_scores.items(), key=lambda item: item[1])}
        nearest_users_list = list(sorted_nearest_users_dict.keys())
        nearest_users_list.reverse()
        return nearest_users_list

    def get_common_movies(self, user_to_compare, nearest_user):
        '''
        Function getting movies common for compared users
        Parameters:
        user_to_compare (str): user to compare
        nearest_user (str): near user
        Returns:
        movies: common films
        '''
        common_movies = []
        i = 0
        for item in self.data[user_to_compare]:
            i += 1
            if item in self.data[nearest_user]:
                common_movies.append(item)
        return common_movies

    def recommended_movies(self):
        '''
        function returns the 5 most recommended films
        Returns:
        movies: top 5 movies        
        '''
        iterator = 0
        recommended_movies = []
        nearest_list = self.get_nearest_users_list(self.user)
        while len(recommended_movies) < 5:
            nearest = nearest_list[iterator]
            if nearest not in self.most_compatible_users:
                self.most_compatible_users.append(nearest)
            common = self.get_common_movies(self.user, nearest)
            for key, value in data[nearest].items():
                if key not in common and value > 8 and key not in recommended_movies:
                    recommended_movies.append(key)
            iterator += 1
        return recommended_movies[:5]

    def not_recommended_movies(self):
        '''
        function returns the 5 most unrecommended films.
        Returns:
        movies: worst 5 movies    
        '''
        iterator = 0
        not_recomended_movies = []
        nearestList = self.get_nearest_users_list(self.user)
        while len(not_recomended_movies) < 5:
            nearest = nearestList[iterator]
            if nearest not in self.most_compatible_users:
                self.most_compatible_users.append(nearest)
            common = self.get_common_movies(self.user, nearest)
            for key, value in self.data[nearest].items():
                if key not in common and value < 3:
                    not_recomended_movies.append(key)
            iterator += 1
        return not_recomended_movies[:5]

    def get_most_compatible_users(self):
        return self.most_compatible_users


def toString(dataList):
    i = 1
    for item in dataList:
        print(i, ". ", item)
        i += 1


with open('ratings.json', 'r', encoding="utf-8") as f:
    data = json.loads(f.read())

user = "Paweł Czapiewski"
rSystem = RecommendationSystem(data, user)

print("Polecane: ")
toString(rSystem.recommended_movies())
print("Lepiej unikac: ")
toString(rSystem.not_recommended_movies())
print("Pdobony gust maja:")
toString(rSystem.get_most_compatible_users())