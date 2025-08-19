#!/usr/bin/env python
"""Main entry point for the Document Reader application."""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from app.main import start
from config.settings import settings
from config.loader import update_settings_from_yaml


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Document Reader API")
    parser.add_argument(
        "--host",
        type=str,
        default=settings.host,
        help=f"Host to bind the server to (default: {settings.host})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.port,
        help=f"Port to bind the server to (default: {settings.port})"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=settings.debug,
        help="Enable debug mode"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=settings.output_directory,
        help=f"Directory to store output files (default: {settings.output_directory})"
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_args()
    
    # Load configuration from YAML file
    update_settings_from_yaml()
    
    # Command line arguments override configuration file
    settings.host = args.host
    settings.port = args.port
    settings.debug = args.debug
    settings.output_directory = args.output_dir
    
    # Configure logging
    log_level = logging.DEBUG if settings.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Start the application
    start()


if __name__ == "__main__":
    main()