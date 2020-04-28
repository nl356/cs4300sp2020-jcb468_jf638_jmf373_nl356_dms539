from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
from movies.movies import read_movies_json
from songs.songs import read_songs_json
from tfidf import read_tfidf_matrix

def get_cos_sim(songID, movID, movie_and_songs_by_words):   
    """
    Returns the cosine similarity score between a given song title and movie title 
    """
    songTfIdf = movie_and_songs_by_words[songID]
    movTfIdf = movie_and_songs_by_words[movID]
    dot_product = np.dot(songTfIdf,movTfIdf)
    
    return dot_product

def main_search(song_title, num_movies_to_output):
  """
	Returns num_movies_to_output movies most similar to given song in the form:
   [(sim_score:float, mov:json entry dict), ...]  
  Input song_title: string , int num_movies_to_output 
	"""
  print("search: Start loading Data")
  movieData = read_movies_json()
  songData = read_songs_json()
  matrix = read_tfidf_matrix()
  print("search: Done loading Data")
  
  song_name_to_index = {}
  j = len(movieData)
  for songDict in songData:
    song_name_to_index[songDict["name"]]=j
    j=j+1

  songID = song_name_to_index[song_title]
  song_sent = songData[songID-len(movieData)]["lyrics_sentiment"] #Gets the sentiment of the song

  sim_scores = []
  movID = 0
  for movie in movieData:
    # All scores between 1-10
    sim_score = (get_cos_sim(songID, movID, matrix)) * 25
    rating_factor = movie["rating"]
    movie_sent = movie["description_sentiment"] #Gets the sentiment of the movie
    sentiment_factor = (2 - np.abs(song_sent - movie_sent)) * 5
    # sentiment_factor = 1
    score = 0.7*sim_score + 0.1*rating_factor +  0.2*sentiment_factor
    sim_scores.append((score, movie))
    movID = movID+1

  # Normalize by max score 
  # max_score = np.sqrt(10)*2
  # max_score = 0.8*0.5 + 0.1*10 +  0.1*10
  # for i in range(len(sim_scores)):
  #   sim_scores[i]=(sim_scores[i][0]/max_score, sim_scores[i][1])
    
  sorted_by_sim = sorted(sim_scores, reverse = True, key = lambda x: x[0])[0:num_movies_to_output]

  return sorted_by_sim