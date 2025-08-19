"""Application settings."""

import os
from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings.
    
    This class uses Pydantic's BaseSettings to load configuration from environment
    variables and/or a configuration file.
    """
    
    # API server settings
    host: str = Field(default="0.0.0.0", env="API_HOST")
    port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Application settings
    project_name: str = Field(default="Document Reader", env="PROJECT_NAME")
    output_directory: str = Field(
        default=str(Path(os.getcwd()) / "outputs"),
        env="OUTPUT_DIRECTORY"
    )
    
    # Default technology
    default_technology: str = Field(default="tesseract", env="DEFAULT_TECHNOLOGY")
    
    # Technology-specific settings
    technology_settings: Dict[str, Dict] = Field(default_factory=dict)
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Create settings instance
settings = Settings()


def load_config_from_file(config_path: Optional[str] = None) -> None:
    """Load configuration from a file.
    
    Args:
        config_path: Path to the configuration file
    """
    # This is a placeholder for loading configuration from a file
    # In a real implementation, this would load YAML/JSON config
    pass


def reload_config() -> None:
    """Reload configuration."""
    # This is a placeholder for reloading configuration
    # In a real implementation, this would reload the configuration
    pass