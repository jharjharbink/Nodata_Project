from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Date)

from NodataScraper.settings import DATABASE_URI

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(DATABASE_URI)


def create_table(engine):
    Base.metadata.create_all(engine)


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    artist = Column(String)
    album = Column(String)
    album_creation_year = Column(Integer)
    label = Column(String)
    tags = Column(String)
    published_date = Column(Date)
    comment_number = Column(Integer)
    album_url = Column(String)
    image_urls = Column(String)

    def __repr__(self):
        return f"<Album(id={id}, " \
               f"artist='{self.artist}', " \
               f"album='{self.album}', " \
               f"album_creation_year={self.year}, " \
               f"label={self.label}, " \
               f"tags={self.tags}, " \
               f"published_date={self.published}, " \
               f"comment_number={self.comment_number}, " \
               f"album_url={self.album_url}, " \
               f"image_urls={self.image_urls})>"