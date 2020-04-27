import json
from textblob import TextBlob

def read_songs_json():
  """
  Returns a list of song dicts from `songs.json` of form:
    name: string
    artists: string
    date: string
    genre: list of string
    genre_sentiment: float
    lyrics: string
    lyrics_sentiment: float
  """
  with open('./songs/songs.json', 'r') as f:
    song_data = json.load(f)

  return song_data


def add_songs_sentiments():
	songs = read_songs_json()

	for song in songs:
		song["lyrics_sentiment"] = round(TextBlob(song["lyrics"]).polarity, 5)
		song["genre_sentiment"] = round(TextBlob(" ".join(song["genre"])).polarity, 5)

	with open('./songs/songs.json', 'w') as f:
		json.dump(songs, f, indent=4)

		print("Wrote out %i songs" % len(songs))

if __name__ == "__main__":
  read_songs_json()
  add_songs_sentiments()
