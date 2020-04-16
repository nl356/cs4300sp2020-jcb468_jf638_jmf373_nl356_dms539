import json

def read_songs_json():

  with open(‘./songs/songs.json', 'r') as f:
    data = json.load(f)
  return data


if __name__ == "__main__":
  read_songs_json()