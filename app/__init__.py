
import os
from flask import Flask
from app.models import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    environment = os.environ.get("FLASK_ENVIRONMENT", "development")

    if environment == "production":
        app.config.from_object("config.ProductionConfig")
    elif environment == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
