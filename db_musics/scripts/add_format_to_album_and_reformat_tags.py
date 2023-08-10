from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from Tables import Albums
from utility_functions import db_connect

import logging


def map_album_format(format_list):
    if format_list == ['Album', 'Remixes']:
        return 'Remixes'
    elif format_list == ['EP', 'Remixes']:
        return 'Remixes'
    elif format_list == ['Remixes', 'Single']:
        return 'Remixes'
    elif format_list == ['Album', 'EP']:
        return 'EP'
    elif format_list == ['Compilation', 'Remixes']:
        return 'Compilation'
    elif format_list == ['Compilation', 'EP']:
        return 'EP'
    elif format_list == ['Album', 'Compilation']:
        return 'Compilation'
    elif format_list == ['EP', 'Remixes', 'Single']:
        return 'Remixes'
    elif format_list == ['Album', 'Demo']:
        return 'Demo'
    elif format_list == ['Album', 'Single']:
        return 'Single'
    elif format_list == ['EP', 'Single']:
        return 'Single'
    else:
        logging.error(f"new album multiple format detected : {format_list}\nplease register it in map_album_format")


engine = db_connect()
session = sessionmaker(bind=engine)
session = session()

tag_query = select(Albums)
tag_query_result = session.execute(tag_query)

for index, album in enumerate(tag_query_result.scalars()):
    tags = [tag.replace('"', '').replace(' ', '_') for tag in album.tags if tag not in ("Remixes", "Single", "EP", "Album", "Compilation", "Documentary", "Demo", "DVD", "Mixtape"                                                                                                                                                 "")]
    current_format_list = [tag for tag in album.tags if tag in ("Remixes", "Single", "EP", "Album", "Compilation", "Documentary", "Demo", "DVD", "Mixtape")]
    if len(current_format_list) == 0:
        album.tags = tags

    elif len(current_format_list) == 1:
        album.format = current_format_list[0]
        album.tags = tags
    else:
        album.format = map_album_format(current_format_list)
        album.tags = tags

    if index % 100 == 0:
        session.commit()
        print(index)

session.commit()
session.flush()
session.close()