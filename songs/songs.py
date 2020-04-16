import json

def read_songs_json():
  """
  Returns a list of song dicts from `songs.json` of form:
    name: string
    artists: string
    date: string
    genre: list of string
    lyrics: string
  """
  with open('./songs/songs.json', 'r') as f:
    song_data = json.load(f)

  return song_data[:501]

if __name__ == "__main__":
  read_songs_json()