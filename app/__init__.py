from flask import Flask
from app.routes import queue_bp
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["host"] = "0.0.0.0"

    # Регистрация Blueprint
    app.register_blueprint(queue_bp, url_prefix='/queue')

    return app