import random
from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import main_search
from songs.songs import *

song_data = read_songs_json()
song_list = sorted([(song["name"],song["artists"]) for song in song_data])
title_list = sorted([song["name"] for song in song_data])

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = 'Please enter a song title above to see results!'
	else:
		song_title = query[:query.find('(')-1]
		if song_title in title_list:
			data = main_search(song_title)
			output_message = "Search results for the song \"" + song_title + "\" :"
		else:
			data = []
			output_message = "No results for the song \"" + query + "\". Please enter another song title."
	return render_template('search.html', output_message=output_message, data=data, song_list=song_list)