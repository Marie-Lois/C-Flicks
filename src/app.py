import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:lois@localhost/C-Flicks"
db = SQLAlchemy(app)


class All_movies(db.Model):
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
    app.run(debug=True)
