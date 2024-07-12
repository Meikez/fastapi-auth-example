from passlib.context import CryptContext

SECRET_KEY = "supersecretkeyexample123123123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plaintext_password: str, hashed_password: str):
    return pwd_context.verify(plaintext_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def authenticate_user(fake_db: dict, username: str, password: str):
    user = get_user(fake_db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True