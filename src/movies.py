import requests
from app import app, db, All_movies  # Replace 'app' with your actual filename

API_KEY = "ICl6118fFjZFpawF0CoSC2ztZINGqYpPujhmGXyJ"
BASE_URL = "http://www.omdbapi.com/"


def add_movie(title_query):
    response = requests.get(BASE_URL, params={"apikey": API_KEY, "t": title_query})
    data = response.json()

    if data.get("Response") == "False":
        print(f"No movie found: {title_query}")
        return

    title = data.get("Title")
    poster = data.get("Poster")
    genre = data.get("Genre")

    existing = All_movies.query.filter_by(movie_name=title).first()
    if existing:
        print(f"Movie already exists: {title}")
        return

    movie = All_movies(movie_name=title, thumbnail_url=poster, genre=genre)
    db.session.add(movie)
    db.session.commit()
    print(f"Added movie: {title}")


if __name__ == "__main__":
    with app.app_context():  # Required to use db.session outside Flask server
        movies = ["Inception", "Interstellar", "The Matrix", "Titanic"]
        for movie in movies:
            add_movie(movie)
#     db.create_all()
#     print("Database created and movies added.")
