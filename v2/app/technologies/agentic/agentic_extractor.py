"""
Agentic Document Extraction implementation.
Wraps LandingAI Agentic API or library.
"""

from app.core.base import BaseExtractor

class AgenticExtractor(BaseExtractor):
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key

    def run(self, image):
        # TODO: implement agentic document extraction call
        pass
