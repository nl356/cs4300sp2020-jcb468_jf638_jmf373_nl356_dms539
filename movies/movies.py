import json
import csv
from textblob import TextBlob
from imdb import IMDb, IMDbError


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
		imdb_id: string
		name: string
		description: string
		description_sentiment: float
		year: int
		genres: list of string
		genres_sentiment: float
		rating: float
	"""
	# Read movie data from CSV
	with open("./movies/IMDb movies.csv", encoding='utf-8') as file:

		rows = csv.reader(file)
		first = True
		movie_jsons = []

		for row in rows:
			
			# Skip column names
			if first:
				first = False
				continue

			# Filter out irrelevant movies (by language, length of description)
			if row[8] != 'English' or len(row[13]) < 75 or len(row[13]) > 250:
				continue

			movie_json = {}

			movie_json["imdb_id"] = row[0]
			movie_json["name"] = row[1]
			movie_json["description"] = row[13]
			movie_json["description_sentiment"] = round(TextBlob(row[13], analyzer=NaiveBayesAnalyzer()).polarity, 5)

			movie_json["year"] = int(row[3])
			movie_json["genres"] = row[5].split(", ")
			movie_json["genres_sentiment"] = round(TextBlob(row[5], analyzer=NaiveBayesAnalyzer()).polarity, 5)

			movie_json["rating"] = float(row[14])

			movie_jsons.append(movie_json)


	# Write movie data to JSON
	with open('./movies/movies.json', 'w') as f:
		json.dump(movie_jsons, f, indent=4)

		print("Wrote out %i movies" % len(movie_jsons))



def get_movie_posters():
	"""
	Retrieves movie poster path from IMDB and appends base path to original JSON
	"""
	ia = IMDb()

	# Read movie data from JSON and append TMDB poster path
	with open('./movies/movies.json', 'r') as f:
		movie_json = json.load(f)

		for i in range(len(movie_json)):
			url = ""
			try:
				m = movie_json[i]
				movie = ia.get_movie(m["imdb_id"][2:])
				url = movie["cover url"]
			except:
				print("No URL for movie at %i" % i)
				pass
			
			m["poster_url"] = url
			# Write to csv back up 
			with open('./movies/posters.csv', 'a+', newline='') as write_obj:
				csv_writer = csv.writer(write_obj)
				csv_writer.writerow([url])
				
			if i%25 == 0:
				print("Retrieved %i movie posters" % i)

	# Write updated data to same JSON
	with open('./movies/movies.json', 'w') as f:
		json.dump(movie_json, f, indent=4)

		print("Added poster path to %i movies" % len(movie_json))



if __name__ == "__main__":
	# DO NOT REWRITE MOVIE JSON UNLESS NECESSARY
	# write_movies_json()
	get_movie_posters()



