# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
用来对items里面提取的数据做进一步处理，如保存等
"""

class BzhanspiderPipeline(object):
    def process_item(self, item, spider):
        return item
