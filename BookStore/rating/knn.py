import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Avg
from rating.models import Rating


class kNNCollaborativeFiltering:
    def __init__(self, k_neighbours):
        self.neighbours = k_neighbours
        self.similarity_matrix = None
        self.users = None

    '''Train model by computing similarity matrix'''
    def fit(self, X_train):
        self.compute_similarity(X_train)

    '''Compute similarity score for each user pair using cosine similarity'''
    def compute_similarity(self, X_train):
        self.users = X_train.index  # Store user IDs
        self.similarity_matrix = cosine_similarity(X_train)  # Use sklearn's cosine similarity

    '''Predict k most similar users based on the given user'''
    def predict(self, user_id, k_neighbours=None):
        if k_neighbours is None:
            k_neighbours = self.neighbours
        
        try:
            loc = self.users.get_loc(user_id)  # Get the location of the user
            
            # Sort neighbours based on similarity, excluding the user itself (hence [1:])
            nearest_neighbours = np.argsort(self.similarity_matrix[loc])[::-1][1:k_neighbours+1]
            
            # Collect recommendations: (user_id, similarity score)
            recommendations = [(self.users[i], self.similarity_matrix[loc][i]) for i in nearest_neighbours]
        except KeyError as e:
            print(f"Error: {e}")
            recommendations = ['User not available in Database']
        
        return recommendations

    '''Get user-product rating matrix'''
    @staticmethod
    def get_user_product_matrix():
        # Query the ratings from the database
        ratings = Rating.objects.values('user_id', 'product_id').annotate(avg_rating=Avg('rate'))

        # Create a pivot table where rows are user IDs, columns are product IDs, and values are ratings
        user_ids = list(ratings.values_list('user_id', flat=True).distinct())
        product_ids = list(ratings.values_list('product_id', flat=True).distinct())

        X_train = np.zeros((len(user_ids), len(product_ids)))

        for rating in ratings:
            user_idx = user_ids.index(rating['user_id'])
            product_idx = product_ids.index(rating['product_id'])
            X_train[user_idx][product_idx] = rating['avg_rating']

        return pd.DataFrame(X_train, index=user_ids, columns=product_ids)
