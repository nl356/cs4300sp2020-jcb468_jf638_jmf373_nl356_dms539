import json
import csv
from textblob import TextBlob


def read_movies_json():
	"""
	Returns a list of movie dicts from `movies.json` of form:
		name: string
		description: string
		description_sentiment: float
		year: int
		genres: list of string
		genres_sentiment: float
		rating: float
	"""
	with open('./movies/movies.json', 'r') as f:
		data = json.load(f)

	print("Retrieved %i movies from movies.json" % len(data))
		
	return data


def write_movies_json():
	"""
	Reads the data from IMDb movies.csv and writes out a json for English movies
	with descriptions between 75 and 250 words. Contains keys:
		name: string
		description: string
		description_sentiment: float
		year: int
		genres: list of string
		genres_sentiment: float
		rating: float
	"""
	# Read movie data from CSV
	with open("./movies/IMDb movies.csv", 'r') as file:

		rows = csv.reader(file)
		first = True
		movie_jsons = []

		for row in rows:

			# Skip column names
			if first:
				first = False
				continue

			# Filter out irrelevant movies (by language, length of description)
			if row[8] != 'English' or len(row[13]) < 75 or len(row[13]) > 250 or int(row[3]) < 2005:
				continue

			movie_json = {}

			movie_json["name"] = row[1]
			movie_json["description"] = row[13]
			movie_json["description_sentiment"] = round(TextBlob(row[13]).polarity, 5)

			movie_json["year"] = int(row[3])
			movie_json["genres"] = row[5].split(", ")
			movie_json["genres_sentiment"] = round(TextBlob(row[5]).polarity, 5)

			movie_json["rating"] = float(row[14])

			movie_jsons.append(movie_json)


	# Write movie data to JSON
	with open('./movies/movies.json', 'w') as f:
		json.dump(movie_jsons, f, indent=4)

		print("Wrote out %i movies" % len(movie_jsons))


if __name__ == "__main__":
	write_movies_json()



