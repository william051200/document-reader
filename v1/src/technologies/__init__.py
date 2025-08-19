"""Technology implementations package.

This package contains implementations of various document processing technologies.
Each technology is implemented as a separate module that registers itself with
the TechnologyFactory.
"""

# Import technologies to register them
from technologies import tesseract, openai