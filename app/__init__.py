from flask import Flask
from app.routes import main
from celery import Celery
import os

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY_BROKER_URL=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        CELERY_RESULT_BACKEND=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    )
    app.register_blueprint(main)
    return app
