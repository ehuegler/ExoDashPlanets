from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import psycopg2
import json
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
            

"""
There will be more code here when the database is setup
It is code for fetching environment variables like the database password
Its necessary since you gotta be careful about API keys in code that might
eventually be part of a public repo
"""
load_dotenv()
db_user = os.environ.get('DB_USER')
db_pswrd = os.environ.get('DB_PSWRD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_database = os.environ.get('DB_DATABASE')


# establishing connection to database
def get_bd_connection():
    connection = psycopg2.connect(user=db_user,
                                    password=db_pswrd,
                                    host=db_host,
                                    port=db_port,
                                    database=db_database)
    return connection







"""
Here is the section of the Flask app that responds to HTTP requests from web browsers
The structure is to define a function that handles each page, then use the decorater
pattern to associate that function to a url that a user might go to (routes are like urls)
"""
@app.route('/')
def index():
    return render_template('index.html', num_planets=num_planets())


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
    conn = get_bd_connection()
    cursor = conn.cursor()
    
    stat = {"Title": "num_planets"}
    
    cursor.execute("""SELECT Count(*) FROM exo_raw""")
    result = cursor.fetchone()[0]

    stat['num_planets'] = result
    
    cursor.close()
    conn.close()
    return stat

# Total number of solar systems with verified exoplanets
@app.route('/api/stat/num_systems')
def num_systems():
    conn = get_bd_connection()
    cursor = conn.cursor()
    
    stat = {"Title": "num_systems"}
    
    cursor.execute("""SELECT Count(DISTINCT hostname) FROM exo_raw""")
    result = cursor.fetchone()[0]

    stat['num_systems'] = result
    
    cursor.close()
    conn.close()
    return stat

# Average number of planets per system
@app.route('/api/stat/avg_num_planets')
def avg_num_planets():
    conn = get_bd_connection()
    cursor = conn.cursor()
    
    stat = {"Title": "avg_num_planets"}

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

    cursor.close()
    conn.close()
    return stat

# Average mass of planets in Earth masse's reported as mass. 
# About a third of the planets don't show up here because they are in mass*sin(inc) units, 
# mass*sin(inc)/sin(inc), or as a mass to radius ratio
@app.route('/api/stat/avg_mass_planet_e')
def avg_mass_planet_e():
    conn = get_bd_connection()
    cursor = conn.cursor()
    
    stat = {"Title": "avg_mass_planet_e"}

    cursor.execute("""select avg(pl_bmasse)
                      from exo_raw""")
    result = cursor.fetchone()[0]

    stat['avg_mass_planet_e'] = result

    cursor.close()
    conn.close()
    return stat

# Average mass of the Stars that contain an Exoplanet
# Reported in Stellar units(1 = Mass of the Sun)
@app.route('/api/stat/avg_mass_star')
def avg_mass_star():
    conn = get_bd_connection()
    cursor = conn.cursor()
    stat = {"Title": "avg_mass_star"}

    cursor.execute("""Select avg(st_mass)
                      from st_data""")
    result = cursor.fetchone()[0]

    stat['avg_mass_star'] = result
    cursor.close()
    conn.close()
    return stat


################################################################
## Visualizations

# returns X column, being the list of unique discovery methods
# Y being the list of the frequency each method was used to discover the verified exoplanets
@app.route('/api/vis/discovery_methods_bar')
def detection_methods_bar():
    conn = get_bd_connection()
    cursor = conn.cursor()
    
    vis = {"Title":"discovery_method"}

    cursor.execute("""select DISTINCT discoverymethod, count(discoverymethod)
                    from exo_raw
                    group by discoverymethod""")
    result = cursor.fetchall()
    X = [row[0] for row in result]
    Y = [row[1] for row in result]

    vis['X'] = X
    vis['Y'] = Y

    cursor.close()
    conn.close()
    return vis

@app.route('/api/vis/stellar_type_pie')
def stellar_type_line():
    conn = get_bd_connection()
    cursor = conn.cursor()
    
    vis = {"Title": "stellar_type"}

    cursor.execute("""with st_type as (select left(upper(st_spectype), 1) as spectype
                      from st_data
                      where st_spectype is not NULL
                      group by st_spectype)

                      select spectype, count(*) 
                      from st_type
                      where spectype in ('O', 'B', 'A', 'F', 'G', 'K', 'M')
                      group by spectype;
                       """)
    result = cursor.fetchall()
    X = [row[0] for row in result]
    Y = [row[1] for row in result]

    vis['X'] = X
    vis['Y'] = Y

    cursor.close()
    conn.close()
    return vis

@app.route('/api/vis/disc_year_line')
def disc_year_line():
    conn = get_bd_connection()
    cursor = conn.cursor()
    
    vis = {"Title": "disc_year"}

    cursor.execute("""select disc_year, count(*)
                    from disc_data
                    group by disc_year
                    order by disc_year
                       """)
    result = cursor.fetchall()
    X = [row[0] for row in result]
    Y = [row[1] for row in result]

    vis['X'] = X
    vis['Y'] = Y

    cursor.close()
    conn.close()
    return vis











