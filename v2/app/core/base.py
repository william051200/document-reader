"""
Abstract base class for all extraction technologies.
Defines a common interface: run(self, image).
"""

from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def run(self, image):
        pass
