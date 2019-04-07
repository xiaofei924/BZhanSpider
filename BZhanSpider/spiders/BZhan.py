# -*- coding: utf-8 -*-
import scrapy
from BZhanSpider.items import BzhanspiderItem

"""
name:scrapy唯一定位实例的属性，必须唯一
allowed_domains：允许爬取的域名列表，不设置表示允许爬取所有
start_urls：起始爬取列表
start_requests：它就是从start_urls中读取链接，然后使用make_requests_from_url生成Request，
                这就意味我们可以在start_requests方法中根据我们自己的需求往start_urls中写入
                我们自定义的规律的链接
parse：回调函数，处理response并返回处理后的数据和需要跟进的url
log：打印日志信息
closed：关闭spider
"""
class BzhanSpider(scrapy.Spider):
    name = 'BZhan'
    allowed_domains = ['www.bilibili.com/']
    start_urls = ['http://www.bilibili.com/video/av48323686']
    # video / av48323686

    """
    start_urls主请求的回调，在里面解析数据并存储到items中去
    """
    def parse(self, response):#默认回调
        print('--------------parse start-----------------')

        # print(response.text)
        item = BzhanspiderItem()
        # title = response.css('.tit tr-fix::text').extract_first()
        title = response.xpath('/html/body/div[3]/div/div[1]/div[1]/h1/span//text()').extract()
        print("---------------------" + str(title))
        item['title'] = title
        yield item

        #获取up主的网页url
        # 取指定第一个加[0], 否则会有type问题
        up_page_url = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/div[1]/a[1]/@href').extract()[0]
        # 获取url绝对路径
        url = response.urljoin(up_page_url)
        print('-------------------' + str(up_page_url))
        print(url)
        yield scrapy.Request(url=url, callback=self.parse_up_page)
        print('--------------parse end-----------------')


    """
    up主的主页请求回调，处理up主的主页的数据
    """
    def parse_up_page(self, response):
        print('-----up_page_parse----: ' + response.text)





