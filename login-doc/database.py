from schemes import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///my_database.db", echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    else:
        return None


def fake_hash_password(password: str):
    return "fakehashed" + password


def decode_token(token):
    user = get_user(users_db,token)
    return user




