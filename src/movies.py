import requests
from app import app, db, All_movies

API_KEY = "d813f52a"
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
            "Prisoners",
            "Sicario",
            "Wind River",
            "The Revenant",
            "Birdman",
            "Whiplash",
            "La La Land",
            "Drive",
            "Nightcrawler",
            "Gone Girl",
            "The Girl with the Dragon Tattoo",
            "The Curious Case of Benjamin Button",
            "The Social Network",
            "Moneyball",
            "Spotlight",
            "The Big Short",
            "The Post",
            "Bridge of Spies",
            "The King's Speech",
            "Darkest Hour",
            "12 Years a Slave",
            "Argo",
            "Lincoln",
            "The Imitation Game",
            "Bohemian Rhapsody",
            "Rocketman",
            "A Beautiful Mind",
            "Cast Away",
            "The Terminal",
            "Catch Me If You Can",
            "The Green Mile",
            "The Pursuit of Happyness",
            "Seven Pounds",
            "Enemy of the State",
            "I Am Legend",
            "Independence Day",
            "Hitch",
            "Focus",
            "Men in Black",
            "Men in Black II",
            "Men in Black III",
            "Kingsman: The Secret Service",
            "Kingsman: The Golden Circle",
            "The Gentlemen",
            "Snatch",
            "Lock, Stock and Two Smoking Barrels",
            "RocknRolla",
            "Sherlock Holmes",
            "Sherlock Holmes: A Game of Shadows",
            "1917",
            "Dunkirk",
            "Hacksaw Ridge",
            "Fury",
            "Pearl Harbor",
            "Enemy at the Gates",
            "The Book Thief",
            "The Pianist",
            "Life Is Beautiful",
            "Hotel Rwanda",
            "Slumdog Millionaire",
        ]

        for movie in movies:
            add_movie(movie)
