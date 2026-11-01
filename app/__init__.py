import os
from flask import Flask
from app.models import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("config.Config")

    # Permite utilizar una configuración diferente durante las pruebas.
    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

    