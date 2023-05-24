# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class MongoDBPipeline(object):

    def __init__(self) -> None:
        self.client = pymongo.MongoClient('localhost', 27017)
        self.collection = self.client['amazon']['bestsellers']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.collection.insert_one(dict(item))
        return f"Total number of products scraped: {self.collection.count_documents({})}"