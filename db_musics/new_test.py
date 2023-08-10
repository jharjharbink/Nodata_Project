from sqlalchemy import create_engine, Column, Integer, String, ARRAY, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Base = declarative_base()
#
#   Table Albums
class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    artist = Column(String)
    album = Column(String)
    album_creation_year = Column(Integer)
    label = Column(String)
    tags = Column(ARRAY(String))
    published_date = Column(Date)
    comment_number = Column(Integer)
    album_url = Column(String)
    image_urls = Column(String)
    format = Column(String)
    image_name = Column(String)


# Table Tags
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


# Table AlbumsTags
class AlbumTag(Base):
    __tablename__ = 'albums_tags'
    album_id = Column(Integer, ForeignKey('albums.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)

    album = relationship('Album', backref='albums_tags')
    tag = relationship('Tag', backref='albums_tags')


# Création de la base de données et des tables
# Base.metadata.create_all(engine)

# Remplissage des tables Tags et AlbumsTags

Session = sessionmaker(bind=engine)
session = Session()

all_tags = set()
for album in session.query(Album):
    all_tags.update(album.tags)

# Insertion des tags dans la table Tags
for tag in all_tags:
    session.add(Tag(name=tag))

# Insertion des associations album/tag dans la table AlbumsTags
for album in session.query(Album):
    for tag_name in album.tags:
        tag = session.query(Tag).filter_by(name=tag_name).one()
        album_tag = AlbumTag(album=album, tag=tag)
        session.add(album_tag)

# Commit des changements
session.commit()