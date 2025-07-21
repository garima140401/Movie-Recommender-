import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your movies data
movies = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies)

# Vectorize
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(movies['tags']).toarray()

# Similarity matrix
similarity = cosine_similarity(vectors)

# Dump similarity from inside PyCharm
import joblib
joblib.dump(similarity, 'similarity.pkl')
