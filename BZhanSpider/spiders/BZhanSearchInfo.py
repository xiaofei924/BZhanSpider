# -*- coding: utf-8 -*-
import logging
from urllib import parse

import scrapy

from BZhanSpider.items import BzhanSearchItem


class BzhansearchinfoSpider(scrapy.Spider):
    name = 'BZhanSearchInfo'
    allowed_domains = ['www.bilibili.com']
    start_urls = ['http://www.bilibili.com/']
    TAG = 'BzhansearchinfoSpider'
    # 搜索关键词
    keywords = ''
    # 默认搜索的url
    search_request_url = 'https://search.bilibili.com/all?keyword=%s'

    # 综合排序
    total_rank_request_url = 'https://search.bilibili.com/all?keyword=%s' \
                             '&from_source=banner_search&order=totalrank&duration=0&tids_1=0'
    # 最多点击
    click_request_url = "https://search.bilibili.com/all?keyword=%s" \
                        "&from_source=banner_search&order=click&duration=0&tids_1=0"
    # 最多弹幕
    dm_request_url = 'https://search.bilibili.com/all?keyword=%s' \
                     '&from_source=banner_search&order=dm&duration=0&tids_1=0'
    # 综合排序path
    total_xpath = '/html/body/div[2]/div[2]/div[2]/div/div[1]/ul[1]/li[1]/a'

    # 最多点击path
    click_xpath = '/html/body/div[2]/div[2]/div[2]/div/div[1]/ul[1]/li[2]/a'

    # 最多弹幕path
    dm_xpath = '/html/body/div[2]/div[2]/div[2]/div/div[1]/ul[1]/li[4]'

    # 下一页path
    next_xpath = '//li[@class="page-item next"]/button'

    spide_page_count = 10

    tab_map = [total_xpath, click_xpath, dm_xpath]
    # tab_map = [total_xpath]

    current_tab = 0

    vlog_map = {}

    def start_requests(self):
        # keywords = getattr(self, 'keywords', None)
        # '网站的编码是gb2312的'
        # keywords = u'红岭'.encode('gb2312')
        # requesturl = "http://bbs.hexun.com/search/?q={0}&type=2&Submit=".format(urllib.quote(keywords))

        # self.keywords = input('请输入要搜索的关键词：\n')
        # if self.keywords is None or len(self.keywords) == 0:
        #     print('关键词不正确！请重新输入')
        #     self.close(self, '关键词不正确！请重新输入')
        self.keywords = '上海 vlog'
        return [scrapy.Request(url=self.search_request_url % parse.quote(self.keywords),
                               meta={'dont_obey_robotstxt ': True},
                               callback=self.parse)]
        # return super().start_requests()

    def parse(self, response):
        # self.log(self.TAG + ', parse')
        # print(response.text)
        item = BzhanSearchItem()
        current_url = response.url
        next = response.xpath(self.next_xpath).extract()
        current_page = response.xpath(
            '//li[@class="page-item active"]/button[@class="pagination-btn num-btn"]/text()').extract_first()
        print('------------------current tab: ' + str(self.current_tab) + ', current_page: ' + str(
            current_page) + ', current url:' + str(current_url) + ' ------------------')
        meta = {'dont_obey_robotstxt ': True}

        for video in response.xpath('//ul[@class="video-contain clearfix"]/li'):
            url = video.xpath('./a/@href').extract_first()
            title = video.xpath('./a/@title').extract_first()
            parse_url = parse.urlparse('http:' + str(url))
            self.vlog_map[parse_url.scheme + '://' + parse_url.netloc + parse_url.path] = title
            item['url'] = 'http:' + str(url)
            item['title'] = str(title)
            # yield item
            print('------------------url: ' + 'http:' + str(url) + ', title: ' + str(title))

        if int(current_page) >= self.spide_page_count or next is None or len(next) is 0:
            self.current_tab += 1
            if self.current_tab <= len(self.tab_map) - 1:
                meta['click_xpath'] = self.tab_map[self.current_tab]
                print('------------------跳转下一个tab：'
                      + str(self.current_tab)
                      + '------------------')
            else:
                print('------------------抓取完成------------------')
                # print(self.vlog_map)
                item['vlog_map'] = self.vlog_map
                yield item
                return
        else:
            meta['click_xpath'] = self.next_xpath
            print('------------------skip next page: %d %s' % (int(current_page) + 1, '------------------'))
        yield scrapy.Request(url=current_url,
                             meta=meta,
                             callback=self.parse,
                             dont_filter=True, )

    # def parse(self, response):
    #     # self.log(self.TAG + ', parse')
    #     pass

    @property
    def logger(self):
        return super().logger()

    def log(self, message, level=logging.DEBUG, **kw):
        super().log(message, level, **kw)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super().from_crawler(crawler, *args, **kwargs)

    def set_crawler(self, crawler):
        super().set_crawler(crawler)

    def _set_crawler(self, crawler):
        super()._set_crawler(crawler)

    def make_requests_from_url(self, url):
        return super().make_requests_from_url(url)

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)

    @classmethod
    def handles_request(cls, request):
        return super().handles_request(request)

    @staticmethod
    def close(spider, reason):
        return super().close(spider, reason)
