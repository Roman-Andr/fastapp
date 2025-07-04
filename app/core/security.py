import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode('utf-8'),
        hashed_password=hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    hashed_password = bcrypt.hashpw(
        password=password.encode('utf-8'),
        salt=bcrypt.gensalt()
    )
    return hashed_password.decode('utf-8')
