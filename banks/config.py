from os import getenv

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_app_config():
    deploy_env = getenv("DEPLOY_ENV", "Developing")

    return {
        "Developing": BaseConfig,
        "Testing": TestingConfig,
        "Production": BaseConfig
    }[deploy_env]
