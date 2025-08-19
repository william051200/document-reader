"""Configuration loader for YAML configuration files."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from config.settings import settings

logger = logging.getLogger(__name__)


def load_yaml_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict[str, Any]: The configuration
    """
    if config_path is None:
        # Look for config.yaml in the config directory
        config_dir = Path(__file__).parent
        config_path = config_dir / "config.yaml"
    
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        logger.info(f"Loaded configuration from {config_path}")
        return config
    
    except Exception as e:
        logger.warning(f"Error loading configuration from {config_path}: {str(e)}")
        return {}


def update_settings_from_yaml(config_path: Optional[str] = None) -> None:
    """Update settings from a YAML configuration file.
    
    Args:
        config_path: Path to the configuration file
    """
    config = load_yaml_config(config_path)
    
    # Update API settings
    if "api" in config:
        if "host" in config["api"]:
            settings.host = config["api"]["host"]
        if "port" in config["api"]:
            settings.port = config["api"]["port"]
        if "debug" in config["api"]:
            settings.debug = config["api"]["debug"]
    
    # Update application settings
    if "app" in config:
        if "project_name" in config["app"]:
            settings.project_name = config["app"]["project_name"]
        if "output_directory" in config["app"]:
            settings.output_directory = config["app"]["output_directory"]
    
    # Update default technology
    if "default_technology" in config:
        settings.default_technology = config["default_technology"]
    
    # Update technology-specific settings
    if "technologies" in config:
        settings.technology_settings = config["technologies"]
    
    logger.info("Updated settings from configuration file")