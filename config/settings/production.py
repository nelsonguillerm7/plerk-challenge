"""Production settings."""

from .base import *  # NOQA
from .base import env  # NOQA
from .modules import MODULES  # NOQA

MIGRATION_MODULES = MODULES
# Base
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]
