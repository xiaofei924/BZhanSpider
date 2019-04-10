# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
"""
用来对items里面提取的数据做进一步处理，如保存等
"""
import json
from openpyxl import Workbook
from scrapy.exporters import CsvItemExporter


class BzhanspiderPipeline(object):
    def __init__(self):
        # pass
        # 初始化一个文件
        self.file_name = open("BZhanInfo.json", "w", encoding='utf-8')

        # 创建excel，填写表头
        self.wb = Workbook()
        self.ws = self.wb.active
        title = ['标题',
                 '栏目（舞蹈、鬼畜、科技等）',
                 '发表时间',
                 '排名',
                 '播放量',
                 '弹幕数',
                 '点赞数',
                 '投币数',
                 '收藏数',
                 '文字介绍',
                 '关键词tag',
                 'UP主与网友互动内容',
                 'UP主',
                 'UP主简介',
                 '认证分类',
                 '关注数',
                 '粉丝数',
                 '播放数']
        self.ws.append(title)

    def process_item(self, item, spider):
        # 这里是将item先转换成字典，在又字典转换成字符串
        # json.dumps转换时对中文默认使用的ascii编码.想输出真正的中文需要指定 ensure_ascii=False
        # 将最后的item 写入到文件中
        text = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file_name.write(text)

        line = [item['title'],
        item['column'],
        item['publish_date'],
        item['ranking'],
        item['play_count'],
        item['danmu_count'],
        item['like_count'],
        item['corn_count'],
        item['favorite_count'],
        item['text_introduce'],
        item['keywords_tag'],
        item['up_comments'],
        item['up_name'],
        item['up_introduction'],
        item['up_certification'],
        item['up_focus_count'],
        item['up_fans_count'],
        item['up_play_count']]
        self.ws.append(line)

        # if spider.is_save:
        #     self.wb.save('BZhanVideoInfo.xlsx')

        return item


# def open_spider(self, spider):
#     self.file = open("BZhanVideoInfo.csv", "wb")
#     self.exporter = CsvItemExporter(self.file, fields_to_export=['标题','栏目（舞蹈、鬼畜、科技等）','发表时间','排名','播放量','弹幕数','点赞数','投币数','收藏数',
#                         '文字介绍','关键词tag','UP主与网友互动内容','UP主','UP主简介','认证分类','关注数','粉丝数','播放数'])
#     self.exporter.start_exporting()
#
# def process_item(self, item, spider):
#     self.exporter.export_item(item)
#     return item
# def close_spider(self, spider):
#     self.exporter.finish_exporting()
#     self.file.close()