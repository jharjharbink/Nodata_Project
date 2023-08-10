import scrapy

from time import sleep
import traceback

from NodataScraper.items import NodataPageItem
from NodataScraper.logger import logger


def test_nodata_album_generateur():
    for i in [188914, 188929, 9]:
        yield f'https://nodata.tv/{i}'


def url_generator():
    with open('C:\\Users\\gusta\\PycharmProjects\\NodataScraper\\NodataScraper\\spiders\\mycsv.csv') as file:
        url_list = [line.rstrip() for line in file]
        return url_list


class NodataGetAlbumUrlSpider(scrapy.Spider):
    name = "nodata_get_album_data"
    start_urls = url_generator()

    def parse(self, responses):
        sleep(1)
        album_url = responses.request.url

        try:
            artist_album_year_and_comment_number = responses.css('h4::text').getall()

            artist_album_and_year = artist_album_year_and_comment_number[1]
            if len(artist_album_year_and_comment_number) > 3:
                comment_number = artist_album_year_and_comment_number[2]
            else:
                comment_number = None
        except:
            logger.info(f'problem with artist_album_and_year:\n{traceback.format_exc()}')

        try:
            imageURL = responses.css('img.attachment-blog_layout_1235_single.size-blog_layout_1235_single.wp-post-image').xpath("@src").extract_first()
        except:
            imageURL=None
            logger.info(f'problem with image:\n{traceback.format_exc()}')

        all_ul_meta_childs = responses.css('ul.meta > li')
        for index, li_tag in enumerate(all_ul_meta_childs):
            try:
                if index == 1:
                    published_date = li_tag.css(f'li::text').get()
                elif index == 2:
                    tags = li_tag.css('li > a::text').getall()
            except:
                logger.info(f'problem with posted_date or tags:\n{traceback.format_exc()}')

        try:
            label = responses.xpath('normalize-space(//span[contains(@class, "aligncenter")]/following-sibling::text())').get()
        except:
            logger(f'problem with label:\n{traceback.format_exc()}')

        yield NodataPageItem(artist_album_and_year=artist_album_and_year, image_urls=imageURL, published_date=published_date,
                             tags=tags, label=label, comment_number=comment_number, album_url=album_url)

