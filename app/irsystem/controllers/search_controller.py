import random
import numpy as np
from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import main_search
from nltk.metrics.distance import edit_distance
from songs.songs import read_songs_json

song_data = read_songs_json()
title_artist_list = sorted([song["name"]+" ("+song["artists"]+")" for song in song_data])
title_list = sorted([song["name"] for song in song_data])

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	year = request.args.get('year')
	rating = request.args.get('rating') 
	dislikeSong = request.args.get('dislikeSong')

	output_message_addendum = ""

	if year == "" or year==None:
		year = None
	else:
		output_message_addendum = " within " + year

	if rating == "" or rating==None:
		rating = None
	elif output_message_addendum != "":
		output_message_addendum += (" and a rating of at least " + rating)
	else:
		output_message_addendum = " with a rating of at least " + rating

	if dislikeSong == None:
		dislikeSong = ""

	if not query:
		data = []
		output_message = 'Please enter a song title above to see results!'
	else:
		song_title = query[:query.find('(')-1]
		if song_title in title_list:

			
			
			if dislikeSong == "":
				data = main_search(song_title, num_movies_to_output=5, year=year, rating=rating, disliked_song_title=None)
				output_message = "Search results for the song \"" + song_title + "\" " + output_message_addendum +":"
			else: 
				dis_song_title = dislikeSong[:dislikeSong.find('(')-1]

				if not dis_song_title in title_list:
					dis_song_title = None
				
				if dis_song_title == song_title:
					output_message = "Please choose a different song you dislike"
					data = []
				else:
					if dis_song_title != None:
						output_message_addendum += (" with disliked song \"" + dis_song_title + "\"")

					data = main_search(song_title, num_movies_to_output=5, year=year, rating=rating, disliked_song_title=dis_song_title)
					output_message = "Search results for the song \"" + song_title + "\" " + output_message_addendum +":"
		else:

			if len(title_list) > 0:
				if "(" in query:
					song_title = query[:query.find('(')-1]
				else:
					song_title = query

				title_no_artist = title_list[0].partition(" (")
				if len(title_no_artist) > 0:
					title_no_artist = title_no_artist[0]
				else:
					title_no_artist = title_list[0]

				min_distance = edit_distance(song_title.lower(), title_no_artist.lower(), transpositions=True)
				replacement_song = title_list[0]

				for title in title_list[1:]:

					title_no_artist = title.partition(" (")
					if len(title_no_artist) > 0:
						title_no_artist = title_no_artist[0]
					else:
						title_no_artist = title

					distance = edit_distance(song_title.lower(), title_no_artist.lower(), transpositions=True)

					if distance < min_distance:
						min_distance = distance
						replacement_song = title

			if min_distance <= 3:

				
				if dislikeSong == "":
					data = main_search(replacement_song, num_movies_to_output=5, year=year, rating=rating, disliked_song_title=None)
					output_message = "We couldn't find \"" + song_title + "\", showing results for \"" + replacement_song + "\" " + output_message_addendum +":"
				else: 
					dis_song_title = dislikeSong[:dislikeSong.find('(')-1]

					if not dis_song_title in title_list:
						dis_song_title = None
					
					if dis_song_title == song_title:
						output_message = "Please choose a different song you dislike"
						data = []
					else:
						if dis_song_title != None:
							output_message_addendum += (" with disliked song \"" + dis_song_title + "\"")

						data = main_search(replacement_song, num_movies_to_output=5, year=year, rating=rating, disliked_song_title=dis_song_title)
						output_message = "We couldn't find \"" + song_title + "\", showing results for \"" + replacement_song + "\" " + output_message_addendum +":"

			else:
				data = []
				output_message = "No results for the song \"" + query + "\". Please enter another song title."
	return render_template('search.html', output_message=output_message, data=data, song_list=title_artist_list)
	# return render_template('search.html', output_message=output_message, data=data, song_list=json.dumps(title_artist_list))