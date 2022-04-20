""" Application Settings """

import os
from pydantic import BaseSettings  # BaseModel,


class Settings(BaseSettings):
    """ Main settings class """
    database_url: str = ""
    log_path: str = "./logs/"
    listening_host: str = "0.0.0.0"
    listening_port: int = 8080
    api_key: str = ""

    class Config:
        """ Load config """
        env_file = os.getenv('BACKEND_ENV', '.env')
        env_file_encoding = 'utf-8'


settings = Settings()

# print(settings.dict())
