"""
Security primitives for authentication.


Rules:
- Never store plaintext passwords
- Never roll your own crypto
- Always use a slow hash (bcrypt)
"""


from passlib.context import CryptContext


# bcrypt is industry standard for password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)




def hash_password(password: str) -> str:
    """
Hash a plaintext password.


This function is intentionally slow to prevent brute-force attacks.
"""
    return pwd_context.hash(password)




def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
Verify a plaintext password against a stored bcrypt hash.


Uses constant-time comparison to avoid timing attacks.
"""
    return pwd_context.verify(plain_password, hashed_password)