import os

from dotenv import load_dotenv

load_dotenv(".env.dev")

basedir = os.path.abspath(os.path.dirname(__file__))

TURSO_DATABASE_URL = os.getenv("DATABASE_URL")
TURSO_AUTH_TOKEN = os.getenv("AUTH_TOKEN")


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = 4000
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CORS_SUPPORTS_CREDENTIALS = True
    SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir, os.getenv("DATABASE_URL")
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


config = os.getenv("MODE")
