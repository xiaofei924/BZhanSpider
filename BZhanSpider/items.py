# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
"""
item 文件用于定义要抓取的数据结构，类似于java bean类
"""

class BzhanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # item定义对应下面的中文
    #下面对应播放界面的item信息
    title = scrapy.Field()#标题
    column = scrapy.Field()#栏目名称
    publish_date = scrapy.Field()#发表时间
    ranking = scrapy.Field()#排名
    play_count = scrapy.Field()#播放量
    danmu_count = scrapy.Field()#弹幕数
    like_count = scrapy.Field()#点赞数
    corn_count = scrapy.Field()#投币数
    favorite_count = scrapy.Field()#收藏数
    text_introduce = scrapy.Field()#文字介绍
    keywords_tag = scrapy.Field()#关键词tag
    up_comments = scrapy.Field()#UP主与网友互动内容

    #以下是另一个url，对应up主界面的item信息
    up_name = scrapy.Field()#up主名字
    up_introduction = scrapy.Field()#up主简介
    up_certification = scrapy.Field()#up主认证分类
    up_focus_count = scrapy.Field()#up主关注数
    up_fans_count = scrapy.Field()#up主粉丝数
    up_play_count = scrapy.Field()#up主播放数


    """
    标题	
    栏目（舞蹈、鬼畜、科技等）	
    发表时间	
    排名	
    播放量	
    弹幕数	
    点赞数	
    投币数	
    收藏数	
    文字介绍	
    关键词tag	
    UP主与网友互动内容	
    UP主	
    UP主简介	
    认证分类	
    关注数	
    粉丝数	
    播放数
    """
