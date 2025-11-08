#app_flask.py is the main file for the headline scraper project using Flask

from flask import Flask, render_template
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Headline

db_path = os.path.join(os.path.dirname(__file__), "headlines.db") #Gets the path to the database
engine = create_engine(f"sqlite:///{db_path}") #Creates the engine for the database
Session = sessionmaker(bind=engine) #Creates the session factory for the database


app = Flask(__name__)

@app.route("/")
def index():
    return "This is the headline scraper project using Flask!"

    
@app.route("/headlines")
def headlines():
    session = Session() #Creates the session for the database
    headlines = session.query(Headline).all()
    #print(headlines)

    html_headlines = "<h1>Headlines</h1> <br> <p>Headline | Polarity | Subjectivity</p>"
    for headline in headlines:
        html_headlines += f"<p>{headline.headline} | {headline.polarity} | {headline.subjectivity} </p>"

    session.close()
    return html_headlines

if __name__ == "__main__":
    app.run(debug=True)