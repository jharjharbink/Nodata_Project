#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8
import sys
from scrapy import cmdline


def main(name):
    if name:
        cmdline.execute(name.split())


if __name__ == '__main__':
    print('[*] beginning main thread')
    name = "nodata_page_number"
    main(name)
    print('[*] main thread exited')
    print('main stop====================================================')