# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re

from itemadapter import ItemAdapter

from NodataScraper.items import NodataDBItem
from NodataScraper.model import db_connect, Album
from NodataScraper.logger import logger

from sqlalchemy.orm import sessionmaker


class NodataScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('artist_album_and_year'):
            artist_album_year_dict = self.artist_album_date_parser(adapter.get('artist_album_and_year'))
        else:
            artist_album_year_dict = {"artist": None, "album": None, "production_year": None}

        if isinstance(adapter.get("label"), str) and len(adapter.get("label")) > 10:
            label = adapter.get("label")[8:].split(' | ')[0]
        else:
            label = None

        if isinstance(adapter.get('comment_number'), str) and " " in adapter.get('comment_number'):
            comment_number = int(adapter.get('comment_number').split()[0])
        else:
            comment_number = 0

        return NodataDBItem(artist=artist_album_year_dict["artist"],
                            album=artist_album_year_dict["album"],
                            album_creation_year=artist_album_year_dict["production_year"],
                            label=label,
                            tags=adapter.get('tags'),
                            published_date=adapter.get('published_date'),
                            comment_number=comment_number,
                            album_url=adapter.get('album_url'),
                            image_urls=adapter.get('image_urls'))

    def artist_album_date_parser(self, string_to_parse):

        returned_dict = dict()

        if " – " in string_to_parse:
            artist_albumAndYear = string_to_parse.split(" – ")
            returned_dict['artist'] = artist_albumAndYear[0]
            album_and_year = artist_albumAndYear[1]

        elif " / " in string_to_parse:
            artist_albumAndYear = string_to_parse.split(" / ")
            returned_dict['artist'] = artist_albumAndYear[0]
            album_and_year = artist_albumAndYear[1]
        else:
            returned_dict['artist'] = None
        logger.debug(f"returned_dict['artist'] = {returned_dict['artist']}")

        if returned_dict['artist'] is not None:
            returned_dict['production_year'] = self.get_creation_year(album_and_year)
            logger.debug(f"production_year'] = {returned_dict['production_year']}")

            if returned_dict['production_year'] is not None:
                returned_dict['album'] = album_and_year[:-6]
            else:
                returned_dict['album'] = album_and_year

        return returned_dict

    @staticmethod
    def get_creation_year(input_text):
        logger.debug(f"entrée danns get_creation_year: input_text = {input_text}")
        pattern = re.compile(r"\[\d+\]$", re.IGNORECASE)
        match = pattern.search(input_text)
        logger.debug(f"match patern/input_text = {match}")
        if match:
            logger.debug(f"valeur retournée = {match.group(0)[1:-1]}")
            return match.group(0)[1:-1]


class NodataInsertDBPipeline:

    def __init__(self):

        engine = db_connect()
        self.session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.session()

        album = Album(artist=item["artist"],
                      album=item["album"],
                      album_creation_year=item["album_creation_year"],
                      label=item["label"],
                      tags=item["tags"],
                      published_date=item["published_date"],
                      comment_number=item["comment_number"],
                      album_url=item["album_url"],
                      image_urls=item["image_urls"])


        try:
            session.add(album)
            session.commit()
            logger.debug("\nInsert OK\n")

        except:
            # session.rollback()
            logger.debug("\n\nproblème d'insert ou de commit en bdd\n\n")

        finally:
            session.close()


