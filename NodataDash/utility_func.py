import json

import requests, logging

from PIL import Image
from io import BytesIO

from dash import dcc, html

from css import *


url = 'http://127.0.0.1:8000/'


def fired_at_page_load(callback_name, args):
    if callback_name == "store_tag":
        if sum(args[:-1]) == 0:
            return True
    elif callback_name == "printing_stored_data":
        if args is None:
            return True
        if len(args["selected_tag_list"]) == 0:
            return True
    return False


def get_tags(tag_type):
    response = requests.post(url=url + 'tags', data={'tag_type': tag_type})  #

    raw_tags = json.loads(response.content)["tags"]
    tags = [tag.replace(" ", "_").replace("'", "_").replace(".", "_") for tag in raw_tags]  # ce traitement doit être côté backend directement dans la bdd
    return tags


def get_grey_tags(tags):
    if len(tags) > 0:
        response = requests.post(url=url + 'grey_tags', data={'tags': tags})
        return json.loads(response.content)["grey_tags"]
    return []


def get_albums(tags):
    if len(tags) > 0:
        response = requests.post(url=url + 'albums', data={'tags': tags})
        try:
            return json.loads(response.content)
        except:
            return []
    return []


def get_tag_name_px_width(tags):
    return [len(tag)*9 for tag in tags]


def set_tag_button_width(tag_name_width):
    current_button_style = white_button_style
    current_button_style['width'] = tag_name_width
    return current_button_style


def str_css_style_mapping(style):
    if style == 'white':
        return white_button_style
    elif style == 'grey':
        return grey_button_style
    elif style == 'green':
        return green_button_style


def set_album_max_length(all_album):
    all_album_artist_length = []
    total_album_artist_length = 0

    for album in all_album:

        artist_album_length = len(album["artist"] + album["album"]) + 3
        year_label_length = len(album["label"]) + 7
        current_max_length = max(artist_album_length, year_label_length)
        total_album_artist_length += current_max_length
        all_album_artist_length.append(current_max_length)

    return all_album_artist_length, total_album_artist_length


def create_div_from_dict(data_dict):
    img_div = None
    if data_dict['image_urls'] is not None:
        try:
            response = requests.get(data_dict['image_urls'])
            img = Image.open(BytesIO(response.content))
            img_div = html.Img(src=data_dict['image_urls'], style={'width': '100%'})
        except:
            pass

    artist_album_div = html.Div(children=[html.Div(f"{data_dict['artist']} - {data_dict['album']}", style={'whiteSpace': 'nowrap', 'overflow': 'hidden', 'textOverflow': 'ellipsis'})])
    album_label_div = html.Div(children=[html.Div(f"{data_dict['album_creation_year']} - {data_dict['label']}", style={'whiteSpace': 'nowrap', 'overflow': 'hidden', 'textOverflow': 'ellipsis'})])
    div_list = [img_div, artist_album_div, album_label_div]
    return html.Div(children=div_list, style={'display': 'flex', 'flex-direction': 'column'})






