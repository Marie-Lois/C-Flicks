import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:lois@localhost/C-Flicks"
db = SQLAlchemy(app)


class All_movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(100), nullable=False)
    thumbnail_url = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(300))

    def to_json(self):
        return {
            "id": self.id,
            "movie_name": self.movie_name,
            "thumbnail_url": self.thumbnail_url,
            "genre": self.genre.split(",") if self.genre else [],
        }


api_key = "ICl6118fFjZFpawF0CoSC2ztZINGqYpPujhmGXyJ"
base_image = "https://image.tmdb.org/t/p/w500"

genre_map = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    18: "Drama",
    10749: "Romance",
    878: "Science Fiction",
    53: "Thriller",
}


@app.route("/")
def hello():
    return "Welcome to C-Flicks!"


@app.route("/add-movie/<string:query>", methods=["POST"])
def add_movie_omdb(query):
    response = requests.get(
        "http://www.omdbapi.com/", params={"apikey": api_key, "t": query}
    )
    data = response.json()

    if data.get("Response") == "False":
        return jsonify({"error": "No movie found"}), 404

    title = data.get("Title")
    poster = data.get("Poster")
    genre = data.get("Genre", "Unknown")

    existing = All_movies.query.filter_by(movie_name=title).first()
    if existing:
        return (
            jsonify({"message": "Movie already exists", "movie": existing.to_json()}),
            200,
        )

    new_movie = All_movies(movie_name=title, thumbnail_url=poster, genre=genre)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify(new_movie.to_json()), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
