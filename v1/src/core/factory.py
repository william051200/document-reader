"""Technology factory for creating technology instances."""

import importlib
import logging
from typing import Dict, Type

from core.base import BaseTechnology

logger = logging.getLogger(__name__)


class TechnologyFactory:
    """Factory for creating technology instances.
    
    This class is responsible for loading and managing technology implementations.
    It uses a registry pattern to keep track of available technologies.
    """
    
    _registry: Dict[str, Type[BaseTechnology]] = {}
    
    @classmethod
    def register(cls, technology_class: Type[BaseTechnology]) -> None:
        """Register a technology implementation.
        
        Args:
            technology_class: The technology class to register
        """
        name = technology_class.get_name()
        cls._registry[name] = technology_class
        logger.info(f"Registered technology: {name}")
    
    @classmethod
    def get_technology(cls, name: str) -> BaseTechnology:
        """Get a technology instance by name.
        
        Args:
            name: The name of the technology
            
        Returns:
            BaseTechnology: An instance of the requested technology
            
        Raises:
            KeyError: If the technology is not found
        """
        if name not in cls._registry:
            # Try to load the technology dynamically
            try:
                module_path = f"technologies.{name}"
                module = importlib.import_module(module_path)
                # The module should register itself in its __init__ method
                if name not in cls._registry:
                    raise KeyError(f"Technology '{name}' not found after loading module")
            except ImportError:
                raise KeyError(f"Technology '{name}' not found")
        
        return cls._registry[name]()
    
    @classmethod
    def list_technologies(cls) -> Dict[str, Dict]:
        """List all registered technologies.
        
        Returns:
            Dict[str, Dict]: A dictionary of technology names and their metadata
        """
        return {
            name: {
                "description": tech_class.get_description(),
                "params": tech_class.get_param_schema()
            }
            for name, tech_class in cls._registry.items()
        }