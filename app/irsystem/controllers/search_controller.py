import random
import numpy as np
from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import main_search
from songs.songs import read_songs_json

song_data = read_songs_json()
title_artist_list = sorted([str(song["name"]+" ("+song["artists"]+")") for song in song_data])
title_list = sorted([song["name"] for song in song_data])

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	year = request.args.get('year')
	rating = request.args.get('rating') 
	dislikeSong = request.args.get('dislikeSong')
	if not query:
		data = []
		output_message = 'Please enter a song title above to see results!'
	else:
		song_title = query[:query.find('(')-1]
		if song_title in title_list:
			data = main_search(song_title, num_movies_to_output=5)
			output_message = "Search results for the song \"" + song_title + "\" :"
		else:
			data = []
			output_message = "No results for the song \"" + query + "\". Please enter another song title."
	return render_template('search.html', output_message=output_message, data=data, song_list=title_artist_list)
	# return render_template('search.html', output_message=output_message, data=data, song_list=json.dumps(title_artist_list))