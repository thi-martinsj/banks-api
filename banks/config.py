from os import getenv

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    pass


class TestingConfig(BaseConfig):
    pass


def get_app_config():
    deploy_env = getenv("DEPLOY_ENV", "Developing")

    return {
        "Developing": BaseConfig,
        "Testing": TestingConfig,
        "Production": BaseConfig
    }[deploy_env]
