from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object(Config)

@app.route('/movies')
def hello():
    return jsonify(movies)

@app.route('/movies', methods=['GET', 'POST'])
def add_movie():
    movie = request.get_json()
    movies.append(movie)
    return jsonify(movies), 200

@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = request.get_json()
    movies[id] = movie
    return jsonify(movies[id]), 200

if __name__ == '__main__':
    app.run(debug=True)