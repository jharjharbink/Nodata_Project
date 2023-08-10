from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    artist = Column(String)
    album = Column(String)
    album_creation_year = Column(Integer)
    label = Column(String)
    published_date = Column(Date)
    comment_number = Column(Integer)
    album_url = Column(String)
    image_urls = Column(String)
    format = Column(String)
    image_name = Column(String)

    def __repr__(self):
        return f"<Album(id={id}, " \
               f"artist='{self.artist}', " \
               f"album='{self.album}', " \
               f"album_creation_year={self.album_creation_year}, " \
               f"label={self.label}, " \
               f"format={self.format}, " \
               f"published_date={self.published_date}, " \
               f"comment_number={self.comment_number}, " \
               f"album_url={self.album_url}, " \
               f"image_urls={self.image_urls}," \
               f"image_name={self.image_name})>"


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tag_type = Column(String)

    def __repr__(self):
        return f"<Tags(id={self.id}, " \
               f"name={self.name}), " \
               f"tag_type={self.tag_type}>"


class AlbumTag(Base):
    __tablename__ = 'albums_tags'
    album_id = Column(Integer, ForeignKey('albums.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    album = relationship('Album', backref='albums_tags')
    tag = relationship('Tag', backref='albums_tags')

    def __repr__(self):
        return f"<AlbumTag(album_id={self.album_id}, tag_id={self.tag_id})>"
