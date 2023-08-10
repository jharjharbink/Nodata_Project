from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update

from Tables import Album, Tag, AlbumTag
from utility_functions import db_connect


engine = db_connect()
session = sessionmaker(bind=engine)
session = session()

# Récupération des tags à mettre à jour
tags = session.query(Tag).all()

# Parcours des tags et mise à jour de la colonne "name"
for tag in tags:
    new_name = tag.name.replace("'", "_").replace('"', '').replace(' ', '_')
    tag.name = new_name

# Enregistrement des modifications
session.commit()


# Recherche des tags contenant des guillemets
tags_to_delete = session.query(Tag).filter(Tag.name.like('%"%')).all()

# Suppression des lignes dans AlbumTag et Tag correspondant aux tags trouvés
for tag in tags_to_delete:
    session.query(AlbumTag).filter(AlbumTag.tag_id == tag.id).delete()
    session.query(Tag).filter(Tag.id == tag.id).delete()

# Commit de la transaction
session.commit()

# Fermeture de la session
session.close()

