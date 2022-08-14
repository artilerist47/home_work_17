from flask import request
from flask_restx import Resource, Namespace

from app.database import db
from app.models import DirectorSchema, Director

directors_ns = Namespace('directors')


director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


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