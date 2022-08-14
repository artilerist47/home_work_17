from flask import Flask
from flask_restx import Api

from app.config import Config
from app.database import db
from app.views.Movies import movies_ns
from app.views.directors import directors_ns
from app.views.genres import genres_ns


def create_app(config: Config) -> Flask:
    applic = Flask(__name__)
    applic.config.from_object(config)
    applic.app_context().push()

    return applic


def configure_app(applic: Flask):
    db.init_app(applic)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    # api = app.config['api']
    # movies_ns = api.namespace('movies')
    # directors_ns = api.namespace('directors')
    # genres_ns = api.namespace('genres')


if __name__ == '__main__':
    app_config = Config
    app = create_app(app_config)
    configure_app(app)
    app.run()
