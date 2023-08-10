from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

from Tables import Album, Tag, AlbumTag
from utility_functions import db_connect


engine = db_connect()
session = sessionmaker(bind=engine)
session = session()

# Création d'une liste contenant les noms des tags à changer
tag_names_to_change = ['Boxset', 'Cut-up/DJ', 'DJ_Mix', 'Album', 'EP', 'Single', 'Compilation', 'Demo', 'Remixes']

# Parcours des tags de la base de données
for tag in session.query(Tag).all():
    if tag.name in tag_names_to_change:
        tag.tag_type = 'format'  # Modification de la valeur de tag_type pour les tags à changer
    else:
        tag.tag = 'style'

# Ajout des tags manquants à la base de données avec tag_type = 'format'
for name in tag_names_to_change:
    existing_tag = session.query(Tag).filter(Tag.name == name).first()
    if not existing_tag:
        new_tag = Tag(name=name, tag_type='format')
        session.add(new_tag)

session.commit()
session.close()
