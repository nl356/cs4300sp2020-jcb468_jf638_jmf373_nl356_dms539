import random
from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import main_search
from songs.songs import *

project_name = "Movie Sound Track"
net_id = "jcb468, jf638, jmf373, nl356, dms539"
song_data = read_songs_json()
song_list = [song["name"] for song in song_data]

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		data = main_search(query)
		output_message = "Search results for the song \"" + query + "\" :"
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, song_list=song_list)



