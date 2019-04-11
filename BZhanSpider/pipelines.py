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

from BZhanSpider.replybean import replybean


class BzhanspiderPipeline(object):
    def __init__(self):
        # pass
        # 初始化一个文件
        self.file_name = open("BZhanInfo.json", "w", encoding='utf-8')

        # 创建excel，填写表头
        self.wb = Workbook()
        self.ws = self.wb.active
        top_title = ['标题',
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
                     '',
                     'UP主与网友互动内容',
                     '',
                     'UP主',
                     'UP主简介',
                     '认证分类',
                     '关注数',
                     '粉丝数',
                     '播放数']
        sub_title = ['',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '网友评论',
                     'UP主回复',
                     '网友互动',
                     '',
                     '',
                     '',
                     '',
                     '',
                     '']
        self.ws.append(top_title)
        self.ws.append(sub_title)
        self.ws.merge_cells(start_row=1, end_row=1, start_column=12, end_column=14)
        self.ws.cell(row=1, column=12, value='UP主与网友互动内容')

    def process_item(self, item, spider):

        print('--------------------- BzhanspiderPipeline, process_item  item: ----------------------\n')
        # print(item)
        if item is None:
            return
        item = dict(item)
        is_commet_or_reply = False

        if 'video_reply_map' in item:
            video_reply_map = item['video_reply_map']
            print('video_reply_map： \n')
            for key in video_reply_map:
                replybean = video_reply_map[key]
                print(replybean.to_string())
            is_commet_or_reply = True

        if 'up_reply_map' in item:
            up_reply_map = item['up_reply_map']
            print('up_reply_map： \n')
            for key in up_reply_map:
                replybean = up_reply_map[key]
                print(replybean.to_string())
            is_commet_or_reply = True

        if 'net_friend_reply_map' in item:
            net_friend_reply_map = item['net_friend_reply_map']
            print('net_friend_reply_map： \n')
            for key in net_friend_reply_map:
                replybean = net_friend_reply_map[key]
                print(replybean.to_string())
            is_commet_or_reply = True

        if not is_commet_or_reply:
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
                    '',
                    '',
                    '',
                    item['up_name'],
                    item['up_introduction'],
                    item['up_certification'],
                    item['up_focus_count'],
                    item['up_fans_count'],
                    item['up_play_count']]
            self.ws.append(line)
        # if spider.is_save:
        self.wb.save('BZhanVideoInfo.xlsx')

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
