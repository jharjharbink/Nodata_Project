import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc, ctx
from dash.exceptions import PreventUpdate

import requests
from css import *
from utility_func import *

import logging, os, json, math

all_style_tags = get_tags('style')
# all_format_tags = get_all_tags('tag')
app = dash.Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div([

    dcc.Store(id="storage"),

    html.Div(id='buttons', children=[
        html.Button(id=f'button_{tag}',
                    children=[tag],
                    n_clicks=0,
                    style=white_button_style,
                    type='filter-dropdown'
                    ) for tag in all_style_tags
    ]),

    html.Div(id='all_albums_container')

])


@app.callback(
    [Output(f'button_{tag}', 'style') for tag in all_style_tags] + [Output(f'storage', 'data')],
    [Input(f'button_{tag}', 'n_clicks') for tag in all_style_tags],
    [State(f'button_{tag}', 'style') for tag in all_style_tags]
)
def button_color_change_and_value_storage(*args):

    # Récupération de l'Input (bouton tag) qui a trigué le  Callback. Servira à déterminer si le bouton a été séléctionné ou déselectionné
    triggered_item = ctx.triggered[0]

    try:
        triggered_tag = triggered_item['prop_id'].split('.')[0][7:]  # récupération de l'id du bouton
        triggered_n_clicks_value = int(triggered_item['value'])  # récupération du nombre de click sur ce bouton
    except:
        log.warning("store_n_clicks --> PreventUpdate")
        raise PreventUpdate  # en cas de callback trigué au démarrage.

    # Récupération de tous les styles actuels des boutons. Servira à déterminer si on doit mettre à jour le style des boutons ou non
    current_tag_style_list = [
        (id_prop.split(".")[0][7:], current_style['background-color'])
        for id_prop, current_style in ctx.states.items()
    ]

    # Détermination par leur style des boutons déjà sélectionnés (peut être également récupéré dans le storage)
    current_green_tags = []
    for tag, style in current_tag_style_list:
        if style == 'green':
            current_green_tags.append(tag)

    # ajout ou suppression du tag associé au bouton qui a trigué.
    if triggered_n_clicks_value % 2 == 0:
        current_green_tags.remove(triggered_tag)
    else:
        current_green_tags.append(triggered_tag)
    current_green_tags.sort()

    # Récupération auprès de l'API des boutons à griser
    grey_tags = get_grey_tags(current_green_tags)

    # fabrication de la liste de styles à retourner, devra être conforté à l'étape d'après
    expected_style_list = []
    for tag in all_style_tags:
        if tag in current_green_tags:
            expected_style_list.append('green')
        elif tag in grey_tags:
            expected_style_list.append('grey')
        else:
            expected_style_list.append('white')

    # Fabrication de la liste retourné contenant les styles des tags à mettre à jour ou des "PreventUpdate"
    returned_list = []
    for (current_tag, current_style), expected_style, tag in zip(current_tag_style_list, expected_style_list, all_style_tags):
        if current_style == expected_style:
            returned_list.append(dash.no_update)
        else:
            returned_list.append(str_css_style_mapping(expected_style))

    # ajout des tags sélectionnés à la liste à retournée pour storage. Servira dans le callback display_album

    returned_list.append(current_green_tags)

    return returned_list


@app.callback(
    Output("all_albums_container", "children"),
    Input("storage", "data"),
)
def display_album(data):

    if not data:
        raise PreventUpdate

    all_albums_container_children = []
    text_div_style = {'text-align': 'center'}
    div_album_container_style = {  # declared her to prevent immutable dict problem
        'display': 'inline-block',
        'align': 'center',
        'width': '20%'
    }

    all_albums = get_albums(data)
    log.warning(data)

    for album_index, current_album in enumerate(all_albums):
        artist = current_album.get('artist', 'no data')
        album = current_album.get('album', 'no data')
        album_creation_year = current_album.get('album_creation_year', 'no data')
        label = current_album.get('label', 'no data')

        image_url = "https://nodatapi.s3.eu-north-1.amazonaws.com/" + current_album["image_name"]

        all_albums_container_children.append(
            html.Div(id=f"album_{album_index}_container", style=div_album_container_style, children=[
                html.Img(id=f"image_album_{album_index}", style=text_div_style, src=image_url),
                html.Div(id=f"artist_album_album_{album_index}", style=text_div_style, children=f"{artist} - {album}"),
                html.Div(id=f"creation_year_label_album_{album_index}", style=text_div_style, children=f"{album_creation_year} - {label}"),
            ]))

    return all_albums_container_children


if __name__ == '__main__':

    # logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    # logging.debug('je vais bien tout va bien')
    log = logging.getLogger("dash_logger")

    app.run_server(debug=True)


