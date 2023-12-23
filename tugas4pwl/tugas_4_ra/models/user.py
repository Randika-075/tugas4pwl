from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
)

from .meta import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    password = Column(Text)
    email = Column(String(255), unique=True)
    role = Column(Text, nullable=True)
    token = Column(Text, nullable=True)


Index("user_email", User.email, unique=True, mysql_length=255)
