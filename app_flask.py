#app_flask.py is the main file for the headline scraper project using Flask

from flask import Flask, render_template
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Headline
from flask import jsonify
from datetime import date
from datetime import datetime
from datetime import timedelta
from sqlalchemy import func
from flask import send_from_directory
from waitress import serve

db_path = os.path.join(os.path.dirname(__file__), "headlines.db") #Gets the path to the database
engine = create_engine(f"sqlite:///{db_path}") #Creates the engine for the database
Session = sessionmaker(bind=engine) #Creates the session factory for the database

STATIC_DATA_DIR = os.path.join(os.path.dirname(__file__), "static", "data")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

    
@app.route("/todays_headlines")
def headlines():
  
    return render_template("todays_headlines.html")

@app.route("/api/todays_headlines")
def api_todays_headlines():
    session = Session() #Creates the session for the database
    #today = date.today()
    latest_timestamp = session.query(func.max(Headline.timestamp)).scalar()
    print(f"The latest timestamp is: {latest_timestamp}")
    # returns a python list of headline objects where the timestamp is today
    headlines = session.query(Headline).filter(Headline.timestamp == latest_timestamp).all()

    #convert the headline objects to a list of dictionaries
    headlines_list = []#This is a list of dictionaries
    for headline in headlines:
        headlines_list.append({
            "timestamp": headline.timestamp,
            "headline": headline.headline,
            "url": headline.url,
            "topic": headline.topic,
            "polarity": headline.polarity,
            "subjectivity": headline.subjectivity,
            "keywords": headline.keywords
        })
    #for debugging
    #print(f"These are the headlines for today: {headlines_list}") 

    #close the session
    session.close()
    return jsonify(headlines_list)

@app.route("/download_data")
def download_data():
    return send_from_directory(STATIC_DATA_DIR, "cnn_headlines.csv", as_attachment=True)

mode = ""

if __name__ == "__main__":
    if mode == "development":
        app.run(debug=True)
    else:
        serve(app, host="0.0.0.0", port=8080, threads=6, connection_limit=100)