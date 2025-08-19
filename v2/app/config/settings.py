"""
Central configuration.
Load from .env or config file.
Includes:
 - server parameters
 - technology parameters
 - save paths
"""

from pydantic import BaseSettings

class Settings(BaseSettings):
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    default_tech: str = "tesseract"

settings = Settings()
