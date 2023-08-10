from django.db import models


class Album(models.Model):
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    album_creation_year = models.IntegerField()
    label = models.CharField(max_length=255)
    published_date = models.DateField()
    comment_number = models.IntegerField()
    album_url = models.CharField(max_length=255)
    image_urls = models.CharField(max_length=255)
    format = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    tag_type = models.CharField(max_length=255)


class AlbumTag(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='albums_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='albums_tags')

    class Meta:
        unique_together = (('album', 'tag'),)
