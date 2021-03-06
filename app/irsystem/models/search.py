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

def main_search(song_title, num_movies_to_output, disliked_song_title = None, year = None, rating = None):
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
  print("Updating Song Data")
  for songDict in songData:
    song_name_to_index[songDict["name"]]=j
    j=j+1

  songID = song_name_to_index[song_title]
  song_sent = songData[songID-len(movieData)]["lyrics_sentiment"] #Gets the sentiment of the song

  if disliked_song_title is not None:
    disliked_songID = song_name_to_index[disliked_song_title]

    sim_scores = []
    movID = 0
    print("Updating Movie Data")
    for movie in movieData:
      # All scores between 1-10
      sim_score = min(10,get_cos_sim(songID, movID, matrix) * 10)
      sim_score_dislike = (get_cos_sim(disliked_songID, movID, matrix)) * -10
      rating_factor = movie["rating"]
      movie_sent = movie["description_sentiment"] #Gets the sentiment of the movie
      sentiment_factor = (2 - np.abs(song_sent - movie_sent)) * 5
      # sentiment_factor = 1
      score = 0.5*sim_score + 0.1*rating_factor +  0.3*sentiment_factor + .1*sim_score_dislike
      sim_scores.append((score, movie))
      movID = movID+1

  else:
    sim_scores = []
    movID = 0
    print("Updating Movie Data")
    for movie in movieData:
      # All scores between 1-10
      sim_score = min(10,get_cos_sim(songID, movID, matrix) * 10)
      rating_factor = movie["rating"]
      movie_sent = movie["description_sentiment"] #Gets the sentiment of the movie
      sentiment_factor = (2 - np.abs(song_sent - movie_sent)) * 5
      score = 0.6*sim_score + 0.1*rating_factor +  0.3*sentiment_factor 
      sim_scores.append((score, movie))
      movID = movID+1
      
  # Normalize score based on Max
  #max_score = max(sim_scores)[0]
  #for i in range(len(sim_scores)):
  #  sim_scores[i]=(round((sim_scores[i][0]/max_score)*10,2), sim_scores[i][1]


  new_sim_scores = []
  for score_movie_tuple in sim_scores:
    if rating is not None:
      if score_movie_tuple[1]["rating"]>=int(rating): 
        if year is not None:
          decade = int(year)-(int(year)%10)
          decade = list(range(decade,decade+10))
          if int(score_movie_tuple[1]["year"]) in decade:
            new_sim_scores.append(score_movie_tuple)
        else:
          new_sim_scores.append(score_movie_tuple)
    else:
      if year is not None:
          decade = int(year)-(int(year)%10)
          decade = list(range(decade,decade+10))
          if int(score_movie_tuple[1]["year"]) in decade:
            new_sim_scores.append(score_movie_tuple)
      else:
        new_sim_scores.append(score_movie_tuple)


  if len(new_sim_scores)<num_movies_to_output:
    num_movies_to_output = len(new_sim_scores)

  sorted_by_sim = sorted(new_sim_scores, reverse = True, key = lambda x: x[0])[0:num_movies_to_output]

  print("Done Search!!!!")
  return sorted_by_sim