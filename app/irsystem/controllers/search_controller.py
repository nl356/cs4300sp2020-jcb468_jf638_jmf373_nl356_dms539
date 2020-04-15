import random
from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from movies.movies import *

project_name = "Movie Sound Track"
net_id = "jcb468, jf638, jmf373, nl356, dms539"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Search results for the song \"" + query + "\" :"
		x = random.randint(0,500)
		data = read_movies_json()[x:x+5]
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



