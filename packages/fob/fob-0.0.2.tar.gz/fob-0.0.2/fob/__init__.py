import logging

# convenience imports
from fob.ingredient import configurable, Ingredient
from fob.store import cacheable

__version__ = "0.0.2"

logging.getLogger(__name__).addHandler(logging.NullHandler())
