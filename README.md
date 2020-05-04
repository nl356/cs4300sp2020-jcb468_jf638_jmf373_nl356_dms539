# Movie Sound Track
Music to Movie Recommendation system <br>
Check out our site: http://moviesoundtrack.herokuapp.com/


CS 4300 Language and Information <br>
Nathalia Lie (nl356), Joseph Fulgieri (jmf373), Julie Barron (jcb468), Daniel Solinsky (dms539), Joe R. Fetter (jf638)



## Table of Contents
### [Quick Start Guide](#quickstart-guide)
### [Flask Template Walk-through](#an-indepth-flask-app-walk-through)


## Quickstart Guide
### 1. Cloning the repository from Git
```bash
git clone https://github.com/CornellNLP/CS4300_Flask_template.git
cd CS4300_Flask_template
```
### 2. Setting up your virtual environment

We assume by now all of you have seen and used virtualenv, but if not, go [here](https://virtualenv.pypa.io/en/stable/installation/) to install and for dead-simple usage go [here](https://virtualenv.pypa.io/en/stable/installation/)

```bash
# Create a new python3 virtualenv named venv.
virtualenv -p python3 venv
# Activate the environment
source venv/bin/activate # (or the equivalent in Windows)

# Install all requirements
pip install -r requirements.txt
```
(For Mac users, you may encounter an `ERROR: Failed building wheel for greenlet`. This can be fixed with `xcode-select --install`.)

An aside note: In the above example, we created a virtualenv for a python3 environment. You will have python3.7.6 installed by default as we have used that version for assignments. This is what we will use for the application as well.

**NOTE:** While you should be able to install these requirements in the virtualenv you used for the assignments, we advise using a fresh virtualenv so you can be sure that your virtualenv's installed packages and your repository's `requirements.txt` match exactly.
This will be important when you add new dependencies.

To add any dependencies for future development just do this:

``` bash
pip install <MODULE_NAME>
pip freeze > requirements.txt
```
### 3. Ensuring environment variables are present

We will be using environment variables to manage configurations for our application.
This is a good practice to hide settings you want to keep out of your public code like passwords or machine-specific configurations.
We will maintain all of our environment variables in a file, and we will populate our environment with these settings before running the app.
We have provided you with starter environment files but remember to add them to your `.gitignore` if you add sensitive information to them.

#### Unix - MacOSx, Linux, Git Bash on Windows
- Your environment variables are stored in a file called `.env`
- To set your environment:
``` bash
source .env
```
- To add a variable to your file, add a line to `.env` with the syntax:
``` cmd
export MY_VARIABLE=SOME_VALUE
```

#### Windows Cmd Prompt
- Your environment variables are stored in a file called `env.bat`
- To set your environment:
``` cmd
call env.bat
```
- To add a variable to your file, add a line to `env.bat` with the syntax:
``` cmd
SET MY_VARIABLE=SOME_VALUE
```

#### autoenv (Optional: Unix systems or Windows Git Bash only)
If you desire, you can set up a tool called `autoenv` so that every time you enter the directory, all environment variables are set immediately. This is handy for hiding configurations that you want to keep out of your public code, like passwords for example. `autoenv` is already installed with the requirements you installed above.
**NOTE: This utility is not critical to the project, it's just nice to have.**
To set up `autoenv`:

``` bash
# Override cd by adding this to your .[?]rc file ([?] = bash, zsh, fish, etc),
# according to your current CLI. I'll use bash in this example:
echo "source `which activate.sh`" >> ~/.bashrc

# Reload your shell
source ~/.bashrc

# Check to see you have a .env file that exists and
# has sets the appropriate APP_SETTINGS and DATABASE_URL variables;
# else create a new file with those variables
cat .env

# This command should produce something non-empty (specifically: config.DevelopmentConfig) if your autoenv is correctly configured
echo $APP_SETTINGS

# Reactivate the environment because you just reloaded the shell
source venv/bin/activate
```
If you are having issues getting autoenv working (echo $APP_SETTINGS returns empty), try running `source .env` from the root directory of your forked repository. This will *manually* set the environment variables. You will have to do this each each time you reopen the terminal.

### 4. Optional: Setting up Postgres Backend (if interested in Postgres)
You may either install the PostgresApp if you are using a Mac [here](https://postgresapp.com/) or [follow the detailed installation guide](https://wiki.postgresql.org/wiki/Detailed_installation_guides) to install it **manually** on your Mac or Windows. Then run the following code after Postgres server is up: **NOTE:** you may find the need to "initialize" a new database through the Postgres App or through the `initdb` command before you are able to proceed with the following commands.
``` bash
# Enter postgres command line interface
$ psql
# Create your database which I will call my_app_db in this example, but you can change accordingly
CREATE DATABASE my_app_db;
# Quit out
\q
```
The above creates the actual database that will be used for this application and the name of the database is `my_app_db` which you can change, but make sure to change the `.env` file and in your production app accordingly which I will talk about lower in this guide.

### 5. Check to see if app runs fine by running in localhost:
``` bash
python3 app.py
```

If you encounter a `KeyError: 'APP_SETTINGS'`, try running `source .env` (Mac) or `call env.bat` (Windows) again.
At this point the app should be running on [http://localhost:5000/](http://localhost:5000/). Navigate to that URL in your browser.

### 6. Push to heroku
We have included a Procfile (*process file*) that leverages gunicorn (which you can read more about [here](https://devcenter.heroku.com/articles/python-gunicorn)) for deployment.

To set up heroku and push this app to it, you must do the following:

1. Install the heroku-cli following the installation instructions found [here](https://devcenter.heroku.com/articles/heroku-cli) and create an account with heroku. (Windows Subsystem for Linux users may find that the Ubuntu command will not work for them and should use the Windows installer instead.)
After that, run the following commands to push to your heroku app into deployment using git from your command line!

``` bash
# Update heroku-cli to its latest version
$ heroku update

# Login with your heroku credentials
$ heroku auth:login
Enter your Heroku credentials:
# You will be directed to a browser login page

# This create logic might be deprecated so
# navigate to Heroku Dashboard and create app manually
$ heroku create <YOUR_WEBSITE_NAME>

# Note you will have had to commit any changes you've made
# since cloning this template in order to push to heroku
$ git push heroku master
```

2. Now, go to your Heroku dashboard and find your app. This will probably be here: `https://dashboard.heroku.com/apps/<YOUR_WEBSITE_NAME>`.

3. You need to modify your environment variables (remember your .env?) by navigating to
`https://dashboard.heroku.com/apps/<YOUR_WEBSITE_NAME>/settings`, clicking `Reveal Config Vars` and in the left box below DATABASE_URL write:
`APP_SETTINGS` and in the box to the right write: `config.ProductionConfig`.

(In essence you are writing `export APP_SETTINGS=config.ProductionConfig` in .env using Heroku's UI. You can also do this from the heroku-cli using the `heroku config:edit` command.)

![](img/app_settings_img.png)

4. You lastly will run: `heroku ps:scale web=1`.
You may now navigate to `https://<YOUR_WEBSITE_NAME>.herokuapp.com` and see your app in production. From now on, you can continue to push to Heroku and have a easy and well-managed dev flow into production. Hooray!

You can check out the example herokuapp: [here](https://thawing-crag-43231.herokuapp.com/)

## Where to go from here?
At some point you will need to fork this repo and name your repo cs4300sp2020-##### with your netids substituting the #####.

To begin customizing this boilerplate webapp to actually do something interesting with your search queries, you should look at modifying the `app/irsystem/controllers/search_controller.py` file where you can see the params we are passing into the rendered view.

If you plan on reading no further than this, please at least skim the section **[An Indepth Flask App Walk-through](#an-indepth-flask-app-walk-through)**, it will provide you a good background on how to interact and modify this template.

* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

## An Indepth Flask App Walk-through
This will overview `Flask` development operations for setting up a new project with an emphasis on the `Model-View-Controller` design pattern. This guide will be utilizing `PostgreSQL` to drive persistent storage on the backend.  

Some of the first few sections will mirror the steps you took in the quickstart guide but will be more in-depth.

### Organization
A `Flask` app has some utility scripts at the top-level, and has a modular organization when defining any sort of functionality.  Dividing up a `Flask` app into modules allows one to separate resource / logic concerns.  

The utility scripts at the top level include the following:

```bash
config.py # describes different environments that app runs in
manage.py # holds functionality for migrating your database (changing its schema)
app.py    # runs the app on a port
```

The entire functional backend of a `Flask` app is housed in a parent module called `app`.  You can create this by creating a directory `app` and populating it with an `__init__.py` file.  Then, inside that `app` directory, you can create modules that describe the resources of your app.  These modules should be as de-coupled and reusable as possible.  For example, let's say I need a bunch of user authentication logic described by a couple of endpoints and helper functions.  These might be useful in another `Flask` app and can be comfortably separated from other functionality.  As a result, I would make a module called `accounts` inside my app directory.  Each module (including `app`) should also have a `templates` directory if you plan on adding any `HTML` views to your app.   

#### Template
The use of templates here is specifically for the purpose of mimicking the structure of an MVC application. In this application, I have separated the system into two separate templates: accounts and irsystem, since some of you might need to leverage the database for user/session log flow so you would only use the irsystem template. The irsystem is what you will be manipulating for the purposes of your information retrevial. If you look at the file `search_controller.py` you can see that we are rendering the view with data being passed in. This data will the results from your IR system which you will customize accordingly. You may make more models/controllers for organization purposes.

### Database Setup
If you followed the quickstart guide, you should now have set up postgres.

Rather than writing raw-SQL for this application, I have chosen to utilize [`SQLAlchemy`](http://flask-sqlalchemy.pocoo.org/2.1/) (specifically, `Flask-SQLAlchemy`) as a database `Object-Relational-Model` (`ORM`, for short).  In addition, for the purposes of serialization (turning these database entities into organized [`JSONs`](http://www.json.org/) that we can send over the wire) and deserialization (turning a `JSON` into a entity once again), I have chosen to use [`Marshmallow`](https://marshmallow-sqlalchemy.readthedocs.io/en/latest/) (specifically, `marshmallow-SQLAlchemy`).

Several modules are needed to completely integrate `Postgres` into a `Flask` app, but several of these modules are co-dependent on one another. I have included all of these in the requirements.txt file, these modules include: flask-migrate marshmallow-sqlalchemy psycopg2.

The migration script, `manage.py`  will be used to capture changes you make over time to the schemas of your various models.  
This script will not work out of the gate and refers to components we have not yet defined in our app, but I will describe these below:

```python
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
  manager.run()
```
In the above, `app` refers to the module we created above in the **File Organization** section.  `db` refers to our reference to the database connection that we have yet to define in the `app` module.  

This script can be used in the following way to migrate your database, on changing your models:
``` bash
# Initialize migrations
python manage.py db init
# Create a migration
python manage.py db migrate
# Apply it to the DB
python manage.py db upgrade
```
You should run these methods after having the .env setup because it requires the APP_SETTINGS and DATABASE_URL to be defined. If you get errors in this section as a result of key-errors for APP_SETTINGS and DATABASE_URL go to the **Environment Variables** section and make sure to delete the migrations folder that is already created with running `python manage.py db init`

### Configuration Setup
Now that we have setup our database and have handled our `manage.py` script, we can create our `config.py` script, which involves the database and various other configuration information specific to `Flask`.  This file will be used in our initialization of the `Flask` app in the `app` module in the near future.  

An example of a `config.py` file that is used in the project looks like this:

``` python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Different environments for the app to run in

class Config(object):
  DEBUG = False
  CSRF_ENABLED = True
  CSRF_SESSION_KEY = "secret"
  SECRET_KEY = "not_this"
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
```

The above defines several classes used to instantiate configuration objects in the creation of a `Flask` app.  Let's go through some of the variables:

* `DEBUG` indicates whether or not debug stack traces will be logged by the server.
* `CSRF_ENABLED`, `CSRF_SESSION_KEY`, and `SECRET_KEY` all relate to `Cross-Site-Request-Forgery`, which you can read more about [here](https://goo.gl/qkGU9).  
* `SQLALCHEMY_DATABASE_URI` refers to the database URL (a server running your database).  In the above example, I refer to an environment variable `'DATABASE_URL'`.  I will be discussing environment variables in the next section, so stay tuned.

### Environment Variables
Environment variables allow one to specify credentials like a sensitive database URL, API keys, secret keys, etc.  These variables can be manually `export-ed` in the shell that you are running your server in, but that is a clunky approach.  The tool [`autoenv`](https://github.com/kennethreitz/autoenv) solves this problem.

`autoenv` allows for environment variable loading on `cd`-ing into the base directory of the project. Follow the following command line arguments to install `autoenv`:

``` bash
# Install the package from pip
pip install autoenv
# Override cd by adding this to your .?rc file (? = bash, zsh, fish, etc), I'll use
echo "source `which activate.sh`" >> ~/.?rc
# Reload your shell
source ~/.?rc
# Make a .env file to hold variables
touch .env
```

As mentioned in the above code, your `.env` file will be where you hold variables, and will look something like this:

``` bash
# Set the environment type of the app (see config.py)
export APP_SETTINGS=config.DevelopmentConfig
# Set the DB url to a local database for development
export DATABASE_URL=postgresql://localhost/my_app_db
```

As you can see above in the example, I reference a specific configuration class (`DevelopmentConfig`), meaning I plan on working in my development environment.  I also have my database URL. Both of which are used heavily in the app. In local mode you will be maniuplating the .env file but in production you will be manipulating the Config Variables in your Heroku instance or you will modify the .env files in your AWS EC2/EB application.

**NOTE:** Now, be sure to `gitignore` your `.env` file.  

### Flask App Setup

Up until now, we haven't been able to run our server.

The configurations of the `Flask` app are contained in `./app/__init__.py`.  The file should look like this:

``` python
# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

# Configure app
socketio = SocketIO()
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
db = SQLAlchemy(app)

# Import + Register Blueprints
# WORKFLOW:
# from app.blue import blue as blue_print
# app.register_blueprint(blue_print)

# Initialize app w/SocketIO
socketio.init_app(app)

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template("404.html"), 404
```

Let's unpack this file piece by piece.  The top initializes `Gevent`, [a coroutine-based Python networking library](http://www.gevent.org/) for `Socket.IO` (a very useful socket library useful in adding real-time sockets to your app).  The next section imports several libraries, initializes our `Flask` app, set our app up with the configurations from the appropriate `config.py` class, creates the `db` connection pool, bootstraps `Socket.IO` to our `Flask` app, and sets the `404` error page that the app should present on not finding a resource.  **NOTE**: the comments regarding registering a "blueprint" will be where we register our sub-modules with our main, parent `Flask` app.  

Since we have involved `Socket.IO` and `Gevent`, you wil see it in requirements.txt

Finally, in order to actually start our server, you will run the  `app.py` script.  This script can be placed at the root of our project:

``` python
from app import app, socketio

if __name__ == "__main__":
  print("Flask app running at http://0.0.0.0:5000")
  socketio.run(app, host="0.0.0.0", port=5000)

```

Now, at the root of your application, you can run:

``` bash
python app.py
```

Your server is now running!

**NOTE:** If you get issues regarding `APP_SETTINGS` or `DATABASE_URL`, you should ensure your `.env` is setup properly, and you should `cd` out of and back into your project root.



Boom! You are done :) How easy was that!
