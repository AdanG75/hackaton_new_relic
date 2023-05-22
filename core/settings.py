import os
from pathlib import Path

from dotenv import load_dotenv

IS_DEPLOYED: bool = True


class Settings(object):
    __MONGO_URI: str
    __SECRET_KEY: str

    def __init__(self):
        if not IS_DEPLOYED:
            env_path = Path('.') / '.env'
            load_dotenv(dotenv_path=env_path)

        self.__MONGO_URI = os.environ.get("MONGO_URI")
        self.__SECRET_KEY = os.environ.get("SECRET_KEY")

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings, cls).__new__(cls)

        return cls.instance

    def get_mongo_uri(self):
        return self.__MONGO_URI

    def get_secret_key(self):
        return self.__SECRET_KEY


setting = Settings()
