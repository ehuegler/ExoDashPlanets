from flask import Flask, render_template
from dotenv import load_dotenv
import os


app = Flask(__name__)

# grab environment variables for connecting to the database
load_dotenv()

@app.route('/')
def home():
    return render_template('index.html')
