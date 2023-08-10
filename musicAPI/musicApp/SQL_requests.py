
def python_list_to_sql_list(a_list):
    return '(' + str(a_list)[1:-1] + ')'


def generate_sql_style_tags():
    return "select tags.name from tags where tags.tag_type = 'style'"


def generate_sql_album_by_tag_strict_search(tag_list):
    """
    Generate the sql to get all albums that have strictly the list of tag passed in parameters
    """

    return f"select * from albums where albums.id in (" \
           f" select at2.album_id " \
           f" from albums_copy ac" \
           f" join albums_tags at2" \
           f" on ac.id = at2.album_id" \
           f" where ac.id in(" \
           f" select albums_tags.album_id" \
           f" from albums_tags"	\
           f" join tags" \
           f" on albums_tags.tag_id = tags.id" \
           f" where tags.name in {python_list_to_sql_list(tag_list)}" \
           f" group by albums_tags.album_id" \
           f" having count(albums_tags.album_id) = {len(tag_list)}" \
           f" )" \
           f" group by at2.album_id" \
           f" having count(at2.album_id) = {len(tag_list)});"


def generate_sql_album_by_tag_soft_search(tag_list):
    """
    Generate the sql to get all albums that have, at least, the list of tags passed in parameters
    """
    return f"select * from albums where albums.id in(" \
            f" select albums_tags.album_id" \
            f" from albums_tags" \
            f" join tags" \
            f" on albums_tags.tag_id = tags.id" \
            f" where tags.name in {python_list_to_sql_list(tag_list)}" \
            f" group by albums_tags.album_id" \
            f" having count(albums_tags.album_id) = {len(tag_list)});"


def generate_sql_grey_tags_search(tag_list):
    # -- Récupère les grey tags à partir des green tags
    # -- Puis on récupère les nom des tags associées aux albums sélectionné dans la requêtes imbriqué, puis la dernière ligne serree à ne pas renvoyer les tags mis en entrée." \
    return f"select distinct tags.name from albums_tags at2" \
           f" join tags" \
           f" on at2.tag_id = tags.id" \
           f" where at2.album_id in (" \
           f" select albums_tags.album_id" \
           f" from albums_tags" \
           f" join tags" \
           f" on albums_tags.tag_id = tags.id" \
           f" where tags.name in {python_list_to_sql_list(tag_list)}" \
           f" group by albums_tags.album_id" \
           f" having count(albums_tags.album_id) = {len(tag_list)})" \
           f" and tags.name not in {python_list_to_sql_list(tag_list)};"

