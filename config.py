
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "manteni-soft-clave-local-2026"
    SQLALCHEMY_DATABASE_URI = "sqlite:///manteni_soft.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
