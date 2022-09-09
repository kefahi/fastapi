""" Application Settings """

import os
from pydantic import BaseSettings  # BaseModel,


class Settings(BaseSettings):
    """Main settings class"""

    app_name: str = "myapp"
    log_path: str = "./logs/"
    listening_host: str = "0.0.0.0"
    listening_port: int = 8080
    api_key: str = ""

    jwt_secret: str = ""
    jwt_algorithm: str = ""
    jwt_access_expires: int = 14400
    jwt_refresh_expires: int = 86400 * 30

    freegeoip_api: str = ""
    mocked_com_api: str = ""

    servername: str = ""

    class Config:
        """Load config"""

        env_file = os.getenv("BACKEND_ENV", ".env")
        env_file_encoding = "utf-8"


settings = Settings()

# print(settings.dict())
