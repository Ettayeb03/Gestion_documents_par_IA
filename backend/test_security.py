from security import hash_password, verify_password, create_access_token

password = "123456"

hashed = hash_password(password)

print("Password :", password)
print("Hash :", hashed)

print(
    verify_password(password, hashed)
)

token = create_access_token(
    {"sub": "admin@gmail.com"}
)

print(token)