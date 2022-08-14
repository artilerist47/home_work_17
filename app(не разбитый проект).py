from flask import Flask, request
from flask_restx import Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    year = fields.Int()
    description = fields.Str()
    trailer = fields.Str()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


api = app.config['api']
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


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


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return directors_schema.dump(db.session.query(Director).all()), 200

    def post(self):
        db.session.add(Director(**director_schema.load(request.json)))
        db.session.commit()
        return "Данные успешно добавлены", 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            return director_schema.dump(db.session.query(Director).filter(Director.id == did).one()), 200
        except Exception as e:
            return str(e), 404

    def put(self, did: int):
        db.session.query(Director).filter(Director.id == did).update(request.json)
        db.session.commit()
        return "Данные успешно обновлены", 201

    def delete(self, did: int):
        db.session.query(Director).filter(Director.id == did).delete()
        db.session.commit()
        return "данные успешно удаленны", 201


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        return genres_schema.dump(db.session.query(Genre).all()), 200

    def post(self):
        db.session.add(Genre(**genre_schema.load(request.json)))
        db.session.commit()
        return "Данные успешно добавлены", 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            return genre_schema.dump(db.session.query(Genre).filter(Genre.id == gid).one()), 200
        except Exception as e:
            return str(e), 404

    def put(self, gid: int):
        db.session.query(Genre).filter(Genre.id == gid).update(request.json)
        db.session.commit()
        return "Данные успешно обновлены", 201

    def delete(self, gid: int):
        db.session.query(Genre).filter(Genre.id == gid).delete()
        db.session.commit()
        return "данные успешно удаленны", 201


if __name__ == '__main__':
    app.run(debug=True)
