from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    description = Column(Text)
    year = Column(Integer)
    rating = Column(Integer)
    genre = Column(Text)
