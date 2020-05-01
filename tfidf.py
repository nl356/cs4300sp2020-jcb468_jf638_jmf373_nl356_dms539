#This script will read in movies and songs from database and return a matrix of tfidf values

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re
import json
from movies.movies import read_movies_json
from songs.songs import read_songs_json
from time import time

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

def build_inverted_index_from_matrix(matrix):
  """Creates an inverted index from a tf-idf matrix
  maps: word index (int) --> list of tuples (document index, occurences of the given word in this doc)
  """
  matrix = matrix.transpose()
  index = {}
  word_index = 0
  doc_index = 0

  for word_col in matrix:
    index[word_index] = []

    for doc_occ in word_col:

      if doc_occ != 0:
        index[word_index].append( (doc_index, doc_occ) )

      doc_index += 1

    doc_index = 0
    word_index += 1

  return index


def build_matrix_from_inverted_index(index, num_movies):
  """Recreates the tf-idf matrix from an inverted index"""
  matrix = np.zeros( ( num_movies, len(index)) )
  w_index = 0

  for word in index:
    for doc_tup in index[word]:
      matrix[doc_tup[0]][w_index] = doc_tup[1]

    w_index += 1

  return matrix



def read_tfidf_matrix():
  """
  Reads the tfidf matrix compressed npy file
  """
  print("Starting read matrix")
  with open('tfidf/tfidf_matrix.npz', 'rb') as f:
    dict_data = np.load(f)
    data = dict_data['arr_0']

  return data
  

def write_matrix():
  """
	Writes compressed npy file containing matrix of tf-idf values
	"""
  movie_and_songs_by_words_matrix = build_matrix()
  np.savez_compressed('tfidf/tfidf_matrix.npz', movie_and_songs_by_words_matrix)


def read_index():
  """reads inverted index"""
  with open('./tfidf/index.json', 'r') as f:
    data = json.load(f)

  print('read index')

  return data


def write_index(index):
  with open('./tfidf/index.json', 'w') as f:
    json.dump(index, f, indent=4)

    print("wrote %i entries" % len(index))


def fetch_cached_matrix():
  """Reads the inverted index and constructs and returns the tf-idf matrix from it"""

  index = read_index()

  ## IF NUMBER OF DATA POINTS CHANGES, HARD CODED VALUE MUST ALSO BE CHANGED
  # I didn't want to read the data to find out it's length in order to save time
  return build_matrix_from_inverted_index(index, 39406)


if __name__ == "__main__":
  write_matrix()
  # # fetch_cached_matrix()

  # print(read_tfidf_matrix().shape)

  # m = build_matrix()

  # x, y, z = np.linalg.svd(m[:1000])

  # print(x.shape)
  # print(y.shape)
  # print(z.shape)






