import uuid
from functools import lru_cache

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    environment = "DEV"
    url = ""
    log_level = ""
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        validate_all = True


class EnvironmentConfig:
    def __init__(self):
        settings = Settings()
        self.environment = settings.environment if settings.environment else None
        self.url = settings.url
        self.log_level = settings.log_level
        self.serialize_logs = False if self.environment == "local" else True
        
        
@lru_cache()
def get_environment_config() -> EnvironmentConfig:
    return EnvironmentConfig()