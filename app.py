"""WSGI compatibility entrypoint. The canonical Flask application lives in main.py."""
from main import app

__all__ = ["app"]
