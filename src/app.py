import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os


load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:lois@localhost/C-Flicks"
db = SQLAlchemy(app)
API_KEY = os.getenv("API_KEY")

BASE_URL = "http://www.omdbapi.com/"


class All_movies(db.Model):
    __tablename__ = "all_movies"
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(300))

    def to_json(self):
        return {
            "id": self.id,
            "movie_name": self.movie_name,
            "thumbnail": self.thumbnail,
            "genre": self.genre.split(",") if self.genre else [],
        }


def add_movie(title_query):
    response = requests.get(BASE_URL, params={"apikey": API_KEY, "t": title_query})

    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")

    data = response.json()
    print(f"Response Data: {data}")

    if data.get("Response") == "False":
        print(f"No movie found: {title_query}")
        return

    title = data.get("Title")
    poster = data.get("Poster")
    genre = data.get("Genre", "Unknown")

    existing = All_movies.query.filter_by(movie_name=title).first()
    if existing:
        print(f"Movie already exists: {title}")
        return

    movie = All_movies(movie_name=title, thumbnail=poster, genre=genre)
    db.session.add(movie)
    db.session.commit()
    print(f"Added movie: {title}")


@app.route("/")
def hello():
    return "Welcome to C-Flicks!"


@app.route("/all-movies", methods=["GET"])
def get_all_movies():
    movies = All_movies.query.all()
    return jsonify([movie.to_json() for movie in movies])


@app.route("/all-movies/<movie_genre>")
def get_movies_by_genre(movie_genre):
    movies = All_movies.query.filter(All_movies.genre.ilike(f"%{movie_genre}%")).all()
    return jsonify([movie.to_json() for movie in movies])
    return movie.to_json()


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

        movies = [
            
        ]

        for movie in movies:
            add_movie(movie)
    app.run(debug=True)
