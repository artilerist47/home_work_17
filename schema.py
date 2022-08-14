from marshmallow import Schema, fields


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