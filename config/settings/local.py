"""Development settings."""

from .base import *  # NOQA
from .base import env  # NOQA
from .modules import MODULES  # NOQA

MIGRATION_MODULES = MODULES
# Base
DEBUG = True
# Security
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH",
)
ALLOWED_HOSTS = ["*"]
