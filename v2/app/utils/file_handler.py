"""
Utility for saving extracted results to files.
Supports configurable file paths and formats.
"""

import json

class FileHandler:
    def save(self, data, file_path: str):
        with open(file_path, "w") as f:
            json.dump(data, f)
