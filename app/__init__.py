from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some-secret-key'

    from app.routes.routes import blueprint

    app.register_blueprint(blueprint)

    app.config['SECRET_KEY'] = 'some-secret-key'

    return app