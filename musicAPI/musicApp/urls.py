from django.urls import re_path
from musicApp.views import TagsAPI, AlbumsAPI, GreyTagsAPI

urlpatterns = [
    re_path(r'^tags$', TagsAPI),
    re_path(r'^albums', AlbumsAPI),
    re_path(r'^grey_tags', GreyTagsAPI)
]

