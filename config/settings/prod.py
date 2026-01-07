from .base import *  # noqa: F403
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"