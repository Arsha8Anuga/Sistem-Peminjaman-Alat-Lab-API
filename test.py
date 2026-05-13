from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

hashed = pwd_context.hash("admin123")

print(hashed)

print(
    pwd_context.verify("admin123", hashed)
)