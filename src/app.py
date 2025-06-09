import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import Swagger
import os


load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

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
    year = db.Column(db.String(200))

    def to_json(self):
        return {
            "id": self.id,
            "movie_name": self.movie_name,
            "thumbnail": self.thumbnail,
            "genre": self.genre.split(",") if self.genre else [],
            "year": self.year,
        }

class User(db.Model):
    __tablename__ = "users"
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique =True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    
    def password_hash(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def user_to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
        


@app.route("/users/sign_up", methods = ["POST"])
def sign():
    username = request.json.get("username")
    email = request.json.get("email")
    password = request.json.get("password")
    
    if not username or not email or not password:
        return jsonify({"error": "Username, email and password are required"}), 400
    else:
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({"error": "Username or email already exists"}), 400
        
        new_user = User(username=username, email=email)
        new_user.password_hash(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "User created successfully", "user": new_user.user_to_json()}), 201



@app.route("/users/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return jsonify({"message": "Login successful", "user": user.user_to_json()}), 200
    else:
        return jsonify({"Invalid username or password"}), 401



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
    release_date = data.get("Year") 

    existing = All_movies.query.filter_by(movie_name=title).first()
    if existing:
        print(f"Movie already exists: {title}")
        return

    movie = All_movies(movie_name=title, thumbnail=poster, genre=genre, year=release_date)
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


@app.route("/all-movies/genre/<movie_genre>")
def get_movies_by_genre(movie_genre):
    movies = All_movies.query.filter(All_movies.genre.ilike(f"%{movie_genre}%")).all()
    return jsonify([movie.to_json() for movie in movies])


@app.route("/all-movies/genre/<genres>")
def get_movies_by_genres(genres):
    genre_list = [genre.strip().lower() for genre in genres.split(",")]

    # Filter movies where any genre matches any genre in genre_list
    movies = All_movies.query.filter(
        db.or_(*[All_movies.genre.ilike(f"%{genre}%") for genre in genre_list])
    ).all()

    return jsonify([movie.to_json() for movie in movies])


@app.route("/all-movies/year/<year_release>")
def get_movie_by_year(year_release):
    movies = All_movies.query.filter_by(year = year_release).all()
    return jsonify([movie.to_json() for movie in movies])

@app.route("/all-movies/search/<movie_name>")
def get_movie_by_name(movie_name):
    movies = All_movies.query.filter(All_movies.movie_name.ilike(f"%{movie_name}%")).all()
    return jsonify([movie.to_json() for movie in movies])
    print(f"Searching for movies with name: {movie_name}")  



if __name__ == "__main__":

    with app.app_context():
        print("Connecting to DB:", app.config["SQLALCHEMY_DATABASE_URI"])
        # db.drop_all()
        db.create_all()

        movies = [
            "World War Z",
            "Inception",
            "Mad Max: Fury Road",
            "Gladiator",
            "Avengers: Endgame",
            "Iron Man",
            "Black Panther",
            "Thor: Ragnarok",
            "Captain America: Civil War",
            "Wonder Woman",
            "The Matrix",
            "Skyfall",
            "No Time to Die",
            "Mission: Impossible – Fallout",
            "The Bourne Identity",
            "John Wick",
            "Edge of Tomorrow",
            "Tenet",
            "The Batman",
            "Dune",
            "Interstellar",
            "Star Wars: A New Hope",
            "Star Wars: The Force Awakens",
            "The Lord of the Rings: The Fellowship of the Ring",
            "The Lord of the Rings: The Return of the King",
            "The Hobbit: An Unexpected Journey",
            "Avatar",
            "Ready Player One",
            "Doctor Strange",
            "Eternals",
            "Coco",
            "Inside Out",
            "Encanto",
            "Moana",
            "Frozen",
            "Finding Nemo",
            "Up",
        ]

        for movie in movies:
            add_movie(movie)
    app.run(debug=True)


# @app.route("/task/display/<int:id>")
# def display_one_task(id):
#     one_task = Task.query.filter_by(id=id).first_or_404()
#     return one_task.to_json()
