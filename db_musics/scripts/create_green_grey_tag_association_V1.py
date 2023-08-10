from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from Tables import TagAlbumId, Tags, TagSetMapping

from utility_functions import db_connect, drop_and_create_table


def check_if_set_already_exists(current_set, current_session):
    check_query = current_session.query(TagSetMapping).filter_by(tag_set=current_set).first()
    if check_query is not None:
        return check_query.grey_tags


def update_tags_mapping_set_row(element_as_dict, current_session):
    try:
        current_session.query(TagSetMapping). \
            filter_by(tag_set=element_as_dict["tag_set"]). \
            update({'grey_tags': element_as_dict["grey_tags"]})
    except:
        current_session.rollback()
        raise ValueError(f"something went wrong when updating {element_as_dict} (type: {type(element_as_dict)}")


def set_already_stored(green_tag, grey_tag, current_session):
    request_result = current_session.query(TagSetMapping).where(
        (TagSetMapping.green_tag == green_tag) &
        (TagSetMapping.grey_tag == grey_tag)
    ).first()
    return request_result


def add_set(element_as_dict, current_session):
    element = TagSetMapping(**element_as_dict)
    try:
        current_session.add(element)
    except:
        session.rollback()
        raise ValueError(f"something went wrong when adding {element_as_dict} (type: {type(element_as_dict)}")


engine = db_connect()
session = sessionmaker(bind=engine)
session = session()

# drop_and_create_table(TagSetMapping, engine)

# On récupère toutes les combinaison de "liste de tags" - "liste d'id d'album associé".
#   On s'en servira pour itérer sur toutes les listes de tags
tag_query = select(TagAlbumId)
tagAlbumId_query_result = session.execute(tag_query)

# On créer un dictionnaire avec en clé, le nom du tag, en valeur, son identifiant
# les tags stockés dans la table TagSetMapping sont stockés avec des identifiants
all_tags_query_return = session.query(Tags).all()
all_tags = {tag.tag: tag.id for tag in all_tags_query_return}


# Pour chacune des listes de tag
for index, tag_album_id in enumerate(tagAlbumId_query_result.scalars()):

    # Pour chacun des tags de ces listes de tags
    for current_tag in tag_album_id.tag_list:

        associated_tags = [all_tags[tag] for tag in tag_album_id.tag_list]

        for associated_tag in associated_tags:
            if not set_already_stored(all_tags[current_tag], associated_tag, session):
                add_set({"green_tag": all_tags[current_tag], "grey_tag": associated_tag}, session)

    if index % 100 == 0:
        print(f"{index}/12000 et quelques")
        # session.commit()

# session.commit()
session.close()
