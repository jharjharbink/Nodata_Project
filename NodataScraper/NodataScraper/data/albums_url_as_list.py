
# def find_max_album_id():
#     with open("mycsv.csv", "rt") as f:
#         urls = [url.strip() for url in f.readlines()]
#     ids = [url.split('/')[-1] for url in urls]
#     maximum = max(ids)
#     created_urls = [f'https://nodata.tv/{i}' for i in [9, maximum]]
#
#     ids_set = set(ids)
#     created_urls = set(created_urls)
#
#     intersec = created_urls.intersection(ids_set)
#     print(intersec)

import re
import csv

from NodataScraper.items import NodataPageItem


def get_creation_year(input_text):
    pattern = re.compile(r"\[\d+\]$", re.IGNORECASE)
    match = pattern.search(input_text)
    if match:
        return match.group(0)[1:-1]


def test_artist_album_year_separation():
    test1 = "DJ Y – Cheech Wizard ⁄ Junk Waffle [2022]"
    test2 = "C Mantle / Photisms [2022]"
    test3 = "Miaou / Painted"
    test4 = "gna"

    tests = [test1, test2, test3, test4]

    for test in tests:
        print(test)

        if " – " in test:
            artist_separation = test.split(" – ")
            print(f"Artist: {artist_separation[0]}")
        elif " / " in test:
            artist_separation = test.split(" / ")
            print(f"Artist: {artist_separation[0]}")
        else:
            print(f"NO Artist in : {test}")
            artist_separation = []

        if len(artist_separation) > 0:
            production_year = get_creation_year(artist_separation[1])
            print(f"produced in : {production_year}")

            if production_year:
                album = artist_separation[1][:-6]
            else:
                album = artist_separation[1]
            print(f"Album: {album}")

        print()


def get_url_sample():
    with open('C:\\Users\\gusta\\PycharmProjects\\NodataScraper\\NodataScraper\\spiders\\mycsv.csv') as file:
        return [line.rstrip() for line in file]


gna = get_url_sample()
for gn in gna:
    if not isinstance(gn, str):
        print(type(gn))
        print(gn)
        print()
gna2 = 0
