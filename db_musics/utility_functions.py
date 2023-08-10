from sqlalchemy import delete, select, create_engine, insert

from collections import OrderedDict
from itertools import combinations

from Tables import Album
from config import DATABASE_URI


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(DATABASE_URI)


def check_none_values(session):
    artist_query = select(Album).where((Album.artist is None))
    album_query = select(Album).where((Album.album is None))
    tags_query = select(Album).where((Album.tags is None))
    comment_number_query = select(Album).where((Album.comment_number is None))

    queries = [artist_query, album_query, tags_query, comment_number_query]

    for query in queries:
        result = session.execute(query)

        for album in result.scalars():
            print(album)


def remove_doubled(session):
    all_albums_query = delete(Album).where(Album.id < 16)
    session.execute(all_albums_query)
    session.commit()


class TransfertTableContent:
    def __init__(self, session, engine, table1, table2=None):
        self.session = session
        self.engine = engine
        self.table1 = table1
        self.table2 = table2

    @staticmethod
    def to_list(tags_as_str):
        if tags_as_str is not None:
            return tags_as_str[1:-1].split(',')

    def bind_Album_table(self, row):
        return self.table2(
            id=row.id,
            artist=row.artist,
            album=row.album,
            album_creation_year=row.album_creation_year,
            label=row.label,
            tags=row.tags_list,
            published_date=row.published_date,
            comment_number=row.comment_number,
            album_url=row.album_url,
            image_urls=row.image_urls)

    def operate_transfert(self):
        query = select(self.table1)
        result = self.session.execute(query)
        all_lines = [self.bind_Album_table(row) for row in result.scalars()]
        self.session.add_all(all_lines)
        self.session.commit()


def expose_albums_data(session):
    all_tags = list()  # 210, 203
    all_sets = list()  # 15898 sans la liste filtrante, 12831 avec
    tags_count = OrderedDict()
    ids_by_set = list()  # id_by_set_exemple = [(["Techno", "Trance"], [1, 12, 5093]), ...]
    set_position = 0

    query = select(Albums)
    result = session.execute(query)
    for album in result.scalars():
        tags = [tag.replace('"', '') for tag in album.tags if
                tag not in ["Single", "EP", "Album", "Compilation", "Documentary", "Demo", "DVD"]]
        tags.sort()

        for tag in tags:
            if tag not in all_tags:
                all_tags.append(tag)
            if tag not in tags_count:
                tags_count[tag] = 1
            else:
                tags_count[tag] += 1

        if tags not in all_sets:
            all_sets.append(tags)

        if len(ids_by_set) > 0:
            non_existent_set = True
            for id_set in ids_by_set:

                if tags == id_set[0]:
                    id_set[1].append(album.id)  #
                    non_existent_set = False
            if non_existent_set:
                ids_by_set.append([tags, [album.id]])  #
        else:
            ids_by_set.append([tags, [album.id]])  #

    # print("all_tags :")
    # print(f"number of distinct tags : {len(all_tags)}")
    # for tag in all_tags:
    #     print(tag)
    # print()

    # print("all_sets :")
    # print(f"number of distinct sets : {len(all_sets)}")
    # for tag in all_sets:
    #     print(tag)
    # print()

    tags_count = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)
    print("number of time each tag appears :")
    for index, (tag, tag_count) in enumerate(tags_count):
        if index > 14:
            break
        print(f"{tag} : {tag_count}")

    print()

    ids_by_set.sort(key=lambda tags: len(tags[1]), reverse=True)
    print("ids_by_set :")
    print("number of time each set appears :")
    for index, id_set in enumerate(ids_by_set):
        if index > 14:
            break
        print(f"{id_set[0]} length: {len(id_set[1])}")
    print()


def print_table_content(table, session):
    query = select(table)
    result = session.execute(query)
    for index, album in enumerate(result.scalars()):
        if index > 100:
            break
        print(album)


def drop_and_create_table(table, engine):
    table.__table__.drop(engine)
    table.__table__.create(engine)


def list_key_to_str(list_key):
    return str(list_key)[1:-1].replace(", ", "__")


def generate_get_album_filtered(filter_tag_list, filter_formats):

    filter_tag_list_str = ""
    for tag_index, tag in enumerate(filter_tag_list):
        filter_tag_list_str += "'" + tag + "'"
        if tag_index < len(filter_tag_list) - 1:
            filter_tag_list_str += ", "

    base = f"select * from albums a where " \
           f"a.id in (select unnest(tai.album_id_list) from tag_album_id tai where tai.tag_list = array[{filter_tag_list_str}]::varchar[])" \

    if len(filter_formats) > 0:

        filter_format_base = " a.format like "
        for format_index, format in enumerate(filter_formats):
            if format_index == 0:
                base += " and"
            else:
                base += " or"
            base += filter_format_base + "'" + format + "'"

    base += ';'

    return base


def convert_python_list_to_postgresql_array(tag_list):
    postgresql_array_str = "'{"
    for index, tag in enumerate(tag_list):
        if index != len(tag_list) - 1:
            postgresql_array_str += tag + ', '
        else:
            postgresql_array_str += tag + "}'"
    return postgresql_array_str