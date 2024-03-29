# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from sqlalchemy.orm import sessionmaker
# from models import db_connect, Photos, Tags, create_photo_table, create_Tag_table


import pymongo
from scrapy.exceptions import DropItem


class AutogramPipeline(object):

    # def __init__(self):
    #     engine = db_connect()
    #     create_photo_table(engine)
    #     create_Tag_table(engine)
    #     self.Session = sessionmaker(bind = engine)

    def __init__(self):
        # self.url_seen = set()
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )

        db = self.conn['photos']
        self.collection = db['beach']

    def process_item(self, item, spider):
        dup_check = self.collection.find({'imageURL': item['imageURL']}).count()
        if dup_check == 0:
            self.collection.insert(dict(item))
            print("image Added!")
        else:
            print("Image Exist")
        return item
