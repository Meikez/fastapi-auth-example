from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base


class UserDB(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean)
