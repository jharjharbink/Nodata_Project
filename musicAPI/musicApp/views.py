from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from rest_framework.response import Response
from sqlalchemy import text

from musicApp.models import Album, Tag, AlbumTag
from musicApp.SQL_requests import generate_sql_style_tags, generate_sql_album_by_tag_strict_search, \
    generate_sql_album_by_tag_soft_search, generate_sql_grey_tags_search

from ast import literal_eval

import logging, os


@csrf_exempt
def TagsAPI(request):
    """
    return all tags for display
    """
    if request.method == 'POST':

        tag_type = dict(request.POST)['tag_type'][0]
        logging.debug(f"RECEPTION --> tag_type: {tag_type}")

        all_tags_request = generate_sql_style_tags()

        with connection.cursor() as cursor:
            cursor.execute(all_tags_request)
            tags = [row[0] for row in cursor.fetchall()]

            logging.debug(f"ENVOI --> tags: {tags}")

        return JsonResponse({'tags': tags})


@csrf_exempt
def AlbumsAPI(request):

    # Post method to be able to receive list of strings in request body
    if request.method == 'POST':

        tags = dict(request.POST)['tags']

        search_method = "strict"  # will be replace by below once selection is set on front
        # search_method = dict(request.POST)['search_method']

        if search_method == 'strict':
            get_albums_query = generate_sql_album_by_tag_strict_search(tags)
            # logging.debug(f"strict")

        elif search_method == 'soft':
            get_albums_query = generate_sql_album_by_tag_soft_search(tags)
            # logging.debug(f"soft")

        else:
            # logging.debug(f"ValueError in search method choice")
            raise ValueError

        all_albums = []

        with connection.cursor() as cursor:
            cursor.execute(get_albums_query)
            for row in cursor.fetchall():
                logging.warning(f"row: {row}")

                current_album = dict()
                current_album['artist'] = row[1]
                current_album['album'] = row[2]
                current_album['album_creation_year'] = row[3]
                current_album['label'] = row[4]

                all_albums.append(current_album)

            logging.warning(f"albums: {all_albums}")

        return JsonResponse({'albums': all_albums})


@csrf_exempt
def GreyTagsAPI(request):
    if request.method == 'POST':

        tags = dict(request.POST)['tags']

        get_grey_tags_query = generate_sql_grey_tags_search(tags)
        logging.debug(f"get_grey_tags_query: {get_grey_tags_query}")

        with connection.cursor() as cursor:
            cursor.execute(get_grey_tags_query)
            grey_tags = [row[0] for row in cursor.fetchall()]
            logging.debug(f"query result: {grey_tags}")

        return JsonResponse({'grey_tags': grey_tags})








