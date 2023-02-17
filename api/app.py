from flask import Flask, render_template
from dotenv import load_dotenv
import os


app = Flask(__name__)

"""
There will be more code here when the database is setup
It is code for fetching environment variables like the database password
Its necessary since you gotta be careful about API keys in code that might
eventually be part of a public repo
"""
load_dotenv()






"""
Here is the section of the Flask app that responds to HTTP requests from web browsers
The structure is to define a function that handles each page, then use the decorater
pattern to associate that function to a url that a user might go to (routes are like urls)
"""
@app.route('/')
def index():
    return render_template('index.html', data=num_planets())


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')





"""
Here are the api routes that will actuall do stuff like querying the database
They are not returning html pages, just data. Flask expects these functions
to return dictionaries which it will latter convert to JSON objects
"""
@app.route('/api/num_planets')
def num_planets():
    # this could have a better name than just data
    data = {}
    
    # this is where you would querry the database
    data[num_planets] = 1000
    
    return data