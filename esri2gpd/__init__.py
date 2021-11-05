try:
    from importlib.metadata import version
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    from importlib_metadata import version

from .core import get

__version__ = version(__package__)
