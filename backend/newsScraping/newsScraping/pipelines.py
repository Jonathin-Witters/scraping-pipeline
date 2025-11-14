# Define your item§ pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter._imports import scrapy

from newsScraping.DatabaseManager import DatabaseManager


class ValidationPipeline:
    def process_item(self, item, spider):
        # Check required fields
        required_fields = ["title", "author", "first_lines"]
        for field in required_fields:
            if not item.get(field):
                # Discard the item if any required field is missing
                raise scrapy.exceptions.DropItem(
                    f"Missing {field} in {item.get('url')}"
                )
        return item


class FirestorePipeline:
    def __init__(self):
        self.db = DatabaseManager()

    def process_item(self, item, spider):

        self.db.save_article(item)
        return item
