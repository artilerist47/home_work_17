from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import MovieSchema, Movie

movies_ns = Namespace('movies')


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies_query = db.session.query(Movie)

        if director_id is not None:
            movies_query = movies_query.filter(Movie.director_id == director_id)

        if genre_id is not None:
            movies_query = movies_query.filter(Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        db.session.add(Movie(**movie_schema.load(request.json)))
        db.session.commit()
        return "Данные успешно добавлены", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            return movie_schema.dump(db.session.query(Movie).filter(Movie.id == mid).one()), 200
        except Exception as e:
            return str(e), 404

    def put(self, mid: int):
        db.session.query(Movie).filter(Movie.id == mid).update(request.json)
        db.session.commit()
        return "Данные успешно обновлены", 201

    def delete(self, mid: int):
        db.session.query(Movie).filter(Movie.id == mid).delete()
        db.session.commit()
        return "данные успешно удаленны", 201
