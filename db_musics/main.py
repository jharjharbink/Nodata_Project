from itertools import combinations
import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete, select, insert, create_engine, update

from Tables import Album

from exceptions import SalaryNotInRangeError
from utility_functions import db_connect, print_table_content, drop_and_create_table, TransfertTableContent


engine = db_connect()
session = sessionmaker(bind=engine)
session = session()

for index, album in enumerate(session.query(Album).all()):
    if album.image_urls and not album.image_name:
        image_name = album.image_urls.split("/")[-1]
        album.image_name = image_name
        session.commit()

    if index%100 == 0:
        print(index)

session.close()



