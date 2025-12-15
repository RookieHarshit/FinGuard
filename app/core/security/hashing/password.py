from __future__ import annotations

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from security.hashing.base import get_pepper, apply_pepper, HashingError, Hasher


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=1,
    argon2__hash_len=32,
    argon2__salt_size=16,
)
