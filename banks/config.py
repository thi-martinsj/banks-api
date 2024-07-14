from os import getenv

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "testing"


def get_app_config():
    deploy_env = getenv("DEPLOY_ENV", "Developing")

    return {
        "Developing": BaseConfig,
        "Testing": TestingConfig,
        "Production": BaseConfig
    }[deploy_env]
