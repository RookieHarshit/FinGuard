from __future__ import annotations

from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from typing import Final

from .base import get_pepper
