#This script will read in movies and songs from database and return a matrix of tfidf values

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import json
from movies.movies import read_movies_json
from songs.songs import read_songs_json

def build_vectorizer(max_features, stop_words = 'english', norm='l2'):
    """Returns a TfidfVectorizer object with the above preprocessing properties.
    
    Params: 
    max_features: Integer, build a vocabulary that only consider the top max_features ordered by term frequency across the corpus
    norm: String with default value, Each output row will have unit norm ‘l2’: Sum of squares of vector elements is 1
    stop_words: String with default value, Stop words are words like “and”, “the”, “him”

    Returns: TfidfVectorizer

    Note: consider removing max_features, and adding min_df/max_df
    """
    return TfidfVectorizer(stop_words = stop_words, max_features = max_features, norm = norm)

def build_matrix():
  """
  returns a single matrix of tf-idf values for both movies and songs
  """
  movieData = read_movies_json()
  songData = read_songs_json()
  num_movies = len(movieData)
  num_songs = len(songData)

  word_max = 5000
  movie_and_songs_by_words = np.empty([num_movies+num_songs, word_max])
  tfidf_vec = build_vectorizer(word_max)

  words_list = []
  for i in movieData:
    words_list.append(i["description"])
  for i in songData:
    words_list.append(i["lyrics"])

  movie_and_songs_by_words = tfidf_vec.fit_transform(words_list).toarray()
  return movie_and_songs_by_words

def read_tfidf_matrix():
  """
  Reads the tfidf matrix 
  """
  return np.load('tfidf/tfidf_matrix.npy')
  

def write_matrix():
  """
	Writes txt file containing matrix of tf-idf values
	"""
  movie_and_songs_by_words_matrix = build_matrix()
  np.save('tfidf/tfidf_matrix.npy', movie_and_songs_by_words_matrix)

if __name__ == "__main__":
  write_matrix()