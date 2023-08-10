from itertools import chain, combinations
import logging

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from Tables import TagAlbumId, Tags, TagSetMapping
from utility_functions import db_connect, drop_and_create_table


def add_set(element_as_dict, current_session):
    element = TagSetMapping(**element_as_dict)
    try:
        current_session.add(element)
    except:
        session.rollback()
        raise ValueError(f"something went wrong when adding {element_as_dict} (type: {type(element_as_dict)}")


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))[1:-1]


def get_all_sublist_mapping(my_list):
    all_subset = powerset(my_list)
    return [(subset, tuple(item for item in my_list if item not in subset)) for subset in all_subset]


log = logging.getLogger("dash_logger")

engine = db_connect()
session = sessionmaker(bind=engine)
session = session()

drop_and_create_table(TagSetMapping, engine)


tag_query = select(TagAlbumId)
tagAlbumId_query_result = session.execute(tag_query)


all_tags_query_return = session.query(Tags).all()
all_tags = {tag.tag: tag.id for tag in all_tags_query_return}

too_long_tag_list = []


for index, tag_album_id in enumerate(tagAlbumId_query_result.scalars()):
    log.warning(tag_album_id.tag_list)

    # Pour chacun des tags de ces listes de tags
    if len(tag_album_id.tag_list) < 16:
        tags_as_ids = [all_tags[tag] for tag in tag_album_id.tag_list]

        for (key, value) in get_all_sublist_mapping(tags_as_ids):

            add_set({"green_tag_list": key, "grey_tag_list": value}, session)
        session.commit()

        if index % 100 == 0:
            print(f"{index}/12000 et quelques")

    else:
        too_long_tag_list.append((tag_album_id.id, tag_album_id.tag_list))
session.close()

for item in too_long_tag_list:
    print(item)
    # (9454, ['Abstract', 'Ambient', 'Atmospheric', 'Bass', 'Classical', 'Cumbia', 'Downtempo', 'Drum_n_Bass', 'Dubstep', 'Electronic', 'Experimental', 'Funky', 'Future_Garage', 'House', 'IDM', 'Instrumental', 'Minimal', 'Noise', 'Psychedelic', 'Space_Disco', 'Techno', 'Tribal', 'Tropical', 'UK_Funky', 'UK_Garage', 'Various_Artists'])
