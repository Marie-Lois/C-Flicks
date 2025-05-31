import requests
from dotenv import load_dotenv
from app import app, db, All_movies
import os

load_dotenv()
API_KEY = os.getenv("DATABASE_URL")

BASE_URL = "http://www.omdbapi.com/"


import requests
from dotenv import load_dotenv
from app import app, db, All_movies
import os

load_dotenv()
API_KEY = os.getenv("DATABASE_URL")

BASE_URL = "http://www.omdbapi.com/"


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


if __name__ == "__main__":
    with app.app_context():
        movies = [
            "wonder woman",
            "the dark knight",
            ]

        for movie in movies:
            add_movie(movie)



if __name__ == "__main__":
    with app.app_context():
        movies = [
            "wonder woman",
            "the dark knight",
            ]

        for movie in movies:
            add_movie(movie)
