from flask import current_app as app, request
from flask_restx import Resource

import models
import schema
from models import db

api = app.config['api']
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movie_schema = schema.MovieSchema()
movies_schema = schema.MovieSchema(many=True)
director_schema = schema.DirectorSchema()
directors_schema = schema.DirectorSchema(many=True)
genre_schema = schema.GenreSchema()
genres_schema = schema.GenreSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        movies_query = db.session.query(models.Movie)

        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)

        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        db.session.add(models.Movie(**movie_schema.load(request.json)))
        db.session.commit()
        return "Данные успешно добавлены", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            return movie_schema.dump(db.session.query(models.Movie).filter(models.Movie.id == mid).one()), 200
        except Exception as e:
            return str(e), 404

    def put(self, mid: int):
        db.session.query(models.Movie).filter(models.Movie.id == mid).update(request.json)
        db.session.commit()
        return "Данные успешно обновлены", 201

    def delete(self, mid: int):
        db.session.query(models.Movie).filter(models.Movie.id == mid).delete()
        db.session.commit()
        return "данные успешно удаленны", 201


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return directors_schema.dump(db.session.query(models.Director).all()), 200

    def post(self):
        db.session.add(models.Director(**director_schema.load(request.json)))
        db.session.commit()
        return "Данные успешно добавлены", 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            return director_schema.dump(db.session.query(models.Director).filter(models.Director.id == did).one()), 200
        except Exception as e:
            return str(e), 404

    def put(self, did: int):
        db.session.query(models.Director).filter(models.Director.id == did).update(request.json)
        db.session.commit()
        return "Данные успешно обновлены", 201

    def delete(self, did: int):
        db.session.query(models.Director).filter(models.Director.id == did).delete()
        db.session.commit()
        return "данные успешно удаленны", 201


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        return genres_schema.dump(db.session.query(models.Genre).all()), 200

    def post(self):
        db.session.add(models.Genre(**genre_schema.load(request.json)))
        db.session.commit()
        return "Данные успешно добавлены", 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            return genre_schema.dump(db.session.query(models.Genre).filter(models.Genre.id == gid).one()), 200
        except Exception as e:
            return str(e), 404

    def put(self, gid: int):
        db.session.query(models.Genre).filter(models.Genre.id == gid).update(request.json)
        db.session.commit()
        return "Данные успешно обновлены", 201

    def delete(self, gid: int):
        db.session.query(models.Genre).filter(models.Genre.id == gid).delete()
        db.session.commit()
        return "данные успешно удаленны", 201