from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import GenreSchema, Genre

genres_ns = Namespace('genres')


genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


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