

def python_list_to_sql_list(a_list):
    return '(' + str(a_list)[1:-1] + ')'


def generate_sql_all_tags():
    return "select tags.name from tags"


def generate_sql_album_by_tag_strict_search(tag_list):
    return f"select * from albums where albums.id in (" \
           f"-- dans un deuxième temps, on récupère les albums n'ayant que trois tags" \
           f"select at2.album_id " \
           f"from albums_copy ac" \
           f"join albums_tags at2                                   --la jointure permet d'accéder à la table album_tags pour filtrer (dans les deux dernières lignes de la requête) les albums qui n'y appraissent qui n'ont que trois tags (ceux qu'on a mis en entrée)" \
           f"on ac.id = at2.album_id" \
           f"where ac.id in(" \
           f"" \
           f"--Dans un premier temps, on récupère tous les id d'albums ayant au moins les tags données en entrées"	\
           f"select albums_tags.album_id" \
           f"from albums_tags"	\
           f"join tags                                              -- la jointure permet de travailler avec des listes de string plutot qu'avec des id de tags" \
           f"on albums_tags.tag_id = tags.id" \
           f"where tags.name in {python_list_to_sql_list(tag_list)}  --ici on demande à récupéré toutes les lignes de albums_tags ayant un des tags donnée en entrée" \
           f"group by albums_tags.album_id" \
           f"having count(albums_tags.album_id) = {len(tag_list)}    -- puis on récupère les albums qui apparaissent trois fois (1 fois pour chaque tag)" \
           f")" \
           f"group by at2.album_id" \
           f"having count(at2.album_id) = {len(tag_list)});           --le but de ce group by et having est de prendre uniquement les albums qu'i n'ont que trois tags répertoriées dans albums_tags"


def generate_sql_album_by_tag_soft_search(tag_list):
    return f"-- Récupère tous les albums ayant AU MOINS les tags données" \
            f"select * from albums where albums.id in(" \
            f"select albums_tags.album_id" \
            f"from albums_tags" \
            f"join tags -- la jointure permet de travailler avec des listes de string plutot qu'avec des id de tags" \
            f"on albums_tags.tag_id = tags.id" \
            f"where tags.name in {python_list_to_sql_list(tag_list)} --ici on demande à récupéré toutes les lignes de albums_tags ayant un des tags donnée en entrée"	\
            f"group by albums_tags.album_id" \
            f"having count(albums_tags.album_id) = {len(tag_list)}); -- puis on récupère les albums qui apparaissent trois fois (1 fois pour chaque tag)"	\


def generate_sql_green_tags_search(tag_list):
    return f"-- Récupère les grey tags à partir des green tags" \
           f"select distinct tags.name -- Puis on récupère les nom des tags associées aux albums sélectionné dans la requêtes imbriqué, puis la dernière ligne serree à ne pas renvoyer les tags mis en entrée." \
           f"from albums_tags at2" \
           f"join tags" \
           f"on at2.tag_id = tags.id" \
           f"where at2.album_id in (" \
           f"--Dans un premier temps, on récupère la liste des albums ayant au moins les tags mis en entrée"\
           f"select albums_tags.album_id" \
           f"from albums_tags" \
           f"join tags 							-- la jointure permet de travailler avec des listes de string plutot qu'avec des id de tags" \
           f"on albums_tags.tag_id = tags.id" \
           f"where tags.name in {python_list_to_sql_list(tag_list)} -- ici on demande à récupéré toutes les lignes de albums_tags ayant un des tags donnée en entrée" \
           f"group by albums_tags.album_id" \
           f"having count(albums_tags.album_id) = {len(tag_list)})  -- puis on récupère les albums qui apparaissent trois fois (1 fois pour chaque tag)" \
           f"and tags.name not in {python_list_to_sql_list(tag_list)};"

