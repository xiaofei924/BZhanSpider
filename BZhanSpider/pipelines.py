# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
用来对items里面提取的数据做进一步处理，如保存等
"""
import json


class BzhanspiderPipeline(object):
    def __init__(self):
        # 初始化一个文件
        self.file_name = open("B站视频信息.json", "w", encoding='utf-8')
    def process_item(self, item, spider):
        # 这里是将item先转换成字典，在又字典转换成字符串
        # json.dumps转换时对中文默认使用的ascii编码.想输出真正的中文需要指定 ensure_ascii=False
        # 将最后的item 写入到文件中
        text = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file_name.write(text)
        return item
