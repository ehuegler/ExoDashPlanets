from flask import Flask, render_template
from dotenv import load_dotenv
import psycopg2
import json
import os


app = Flask(__name__)

# establishing connection to database
f = open("../.dbase_conn.json")
conn = json.load(f); f.close();
connection = psycopg2.connect(user=conn['User'],
                                password=conn['Password'],
                                host=conn['Host'],
                                port=conn['Port'],
                                database=conn['Database'])
cursor = connection.cursor()

            

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
################################################################
## Statistics

# Total number of verified exoplanets
@app.route('/api/stat/num_planets')
def num_planets():
    stat = {}
    
    cursor.execute("""SELECT Count(*) FROM exo_raw""")
    result = cursor.fetchone()[0]

    stat['num_planets'] = result
    
    return stat

# Total number of solar systems with verified exoplanets
@app.route('/api/stat/num_systems')
def num_systems():
    stat = {}
    
    cursor.execute("""SELECT Count(DISTINCT hostname) FROM exo_raw""")
    result = cursor.fetchone()[0]

    stat['num_systems'] = result
    
    return stat

# Average number of planets per system
@app.route('/api/stat/avg_num_planets')
def avg_num_planets():
    stat = {}

    cursor.execute("""With pl_per_host as (
                        select hostname, count(pl_name) as pl_count
                        from "ExoDashPlanets".exo_raw
                        group by hostname
                        order by pl_count desc
                      )

                      select round(avg(pl_count), 6)
                      from pl_per_host;""")
    result = float(cursor.fetchone()[0])
    stat['avg_num_planets'] = result

    return stat

# Average mass of planets in Earth masse's reported as mass. 
# About a third of the planets don't show up here because they are in mass*sin(inc) units, 
# mass*sin(inc)/sin(inc), or as a mass to radius ratio
@app.route('/api/stat/avg_mass_planet_e')
def avg_mass_planet_e():
    stat = {}

    cursor.execute("""select avg(pl_bmasse)
                      from exo_raw
                      where pl_bmassprov = 'Mass'""")
    result = cursor.fetchone()[0]

    stat['avg_mass_planet_e'] = result

    return stat


################################################################
## Visualizations

# returns X column, being the list of unique discovery methods
# Y being the list of the frequency each method was used to discover the verified exoplanets
@app.route('/api/vis/discovery_methods_bar')
def detection_methods_bar():
    vis = {}

    cursor.execute("""select DISTINCT discoverymethod, count(discoverymethod)
                    from exo_raw
                    group by discoverymethod""")
    result = cursor.fetchall()
    X = [row[0] for row in result]
    Y = [row[1] for row in result]

    vis['X'] = X
    vis['Y'] = Y

    return vis
    











