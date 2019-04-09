# -*- coding: utf-8 -*-
import json

import scrapy
from BZhanSpider.items import BzhanspiderItem
from selenium import webdriver
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

    # # start_url = input('请输入要抓取B站视频信息的网址, 按回车结束: \n')
    # # https: // api.bilibili.com / x / web - interface / view?aid = 48465492
    # # start_urls = ['https://api.bilibili.com/x/web-interface/view?aid=48465492']#播放界面数据类型json\
    # page_data_url = 'http://www.bilibili.com/video/av48323686'#界面数据，无法获取数量
    # data_url = 'https://api.bilibili.com/x/web-interface/view?aid=48465492'#数据数量(弹幕、播放、点赞等)
    # url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=48465492'#数量json
    # comment_url = 'https://api.bilibili.com/x/v2/reply?callback=jQuery17202434448397650979_1554717195061&jsonp=jsonp&pn=2&type=1&oid=48465492&sort=0&_=1554718673887'
    # # start_urls = [start_url]
    # # video / av48323686


    """
    start_urls主请求的回调，在里面解析数据并存储到items中去
    """
    def parse(self, response):#默认回调
        print('--------------parse start-----------------')

        # print(response.text)
        item = BzhanspiderItem()
        # title = response.css('.tit tr-fix::text').extract_first()
        # title = response.xpath('/html/body/div[3]/div/div[1]/div[1]/h1/span/text()').extract_first()

        title = response.xpath('//span[@class="tit tr-fix"]/text()').extract_first()
        column = response.xpath('//span[@class="a-crumbs"]/a[@target="_blank"]/text()').extract_first()
        publish_date = response.xpath('//div[@class="video-data"]/span[2]/text()').extract_first()
        ranking = ''
        play_count = response.xpath('//div[@class="video-data"]/span[contains(@class,"view")]/text()').extract_first()
        danmu_count = response.xpath('//div[@class="video-data"]/span[@class="dm"]/text()').extract_first()
        like_count = response.xpath('/html/body/div[3]/div/div[1]/div[3]/div[1]/span[1]/text()').extract_first()
        corn_count = response.xpath('/html/body/div[3]/div/div[1]/div[3]/div[1]/span[2]/text()').extract_first()
        text_introduce = response.xpath('/html/body/div[3]/div/div[1]/div[4]/div[1]//text()').extract()
        keywords_tag = response.xpath('/html/body/div[3]/div/div[1]/div[5]/ul//text()').extract()

        if len(text_introduce) > 0:
            text_introduce = '\n'.join(text_introduce)

        if len(keywords_tag) > 0:
            keywords_tag = '\n'.join(keywords_tag)
        # resp = json.loads(response.body, encoding='utf-8')
        # data = resp['data']
        # stat = data['stat']
        # title = data['title']
        # column = ''
        # publish_date = data['pubdate']
        # ranking = ''
        # play_count = stat['view']
        # danmu_count = stat['danmaku']
        # like_count = stat['favorite']
        # corn_count = stat['coin']
        # text_introduce = data['desc']
        # keywords_tag = ''

        #评论先拿第一组数据测试
        up_comments = ''




        # yield item

        #获取up主的网页url
        # 取指定第一个加[0], 否则会有type问题
        up_page_url = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/div[1]/a[1]/@href').extract()[0]
        # 获取url绝对路径
        url = response.urljoin(up_page_url)
        print('-------------------' + str(up_page_url))
        print(url)


        # DEBUG: Filtered offsiterequest to因为Request中请求的URL和allowed_domains中定义的域名冲突，所以将Request中请求的URL过滤掉了，无法请求
        # 在Request请求参数中，设置dont_filter = True, Request中请求的URL将不通过allowed_domains过滤。
        yield scrapy.Request(url=url, callback=self.parse_up_page,dont_filter=True,meta={'title':title,
                                                                                         'column':column,
                                                                                         'publish_date':publish_date,
                                                                                         'ranking':ranking,
                                                                                         'play_count':play_count,
                                                                                         'danmu_count':danmu_count,
                                                                                         'like_count':like_count,
                                                                                         'corn_count':corn_count,
                                                                                         'text_introduce':text_introduce,
                                                                                         'keywords_tag':keywords_tag,
                                                                                         'up_comments':up_comments,


        })

        page_data_url = 'http://www.bilibili.com/video/av48323686'  # 界面数据，无法获取数量
        # yield scrapy.Request(url= page_data_url, callback=self.parse_video_page, dont_filter=True)
        print('--------------parse end-----------------')

    """
    请求当前页的数据
    """
    def parse_video_page(self, response):
        pass

    """
    up主的主页请求回调，处理up主的主页的数据
    """
    def parse_up_page(self, response):
        print('-----------------up_page_parse start------------------')
        # print(response.text)
        # return
        status = response.status
        if status != 200:
            print('request failed, status: ' + status)
            return
        item = BzhanspiderItem();

        title = response.meta['title']
        column = response.meta['column']
        publish_date = response.meta['publish_date']
        ranking = response.meta['ranking']
        play_count = response.meta['play_count']
        danmu_count = response.meta['danmu_count']
        like_count = response.meta['like_count']
        corn_count = response.meta['corn_count']
        text_introduce = response.meta['text_introduce']
        keywords_tag = response.meta['keywords_tag']
        up_comments = response.meta['up_comments']

        up_name = response.xpath('//*[@id="h-name"]/text()').extract_first()
        up_introduction = response.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/h4/text()').extract_first()
        up_certification = response.xpath('//*[@id="h-ceritification"]/text()').extract_first()
        up_focus_count = response.xpath('//*[@id="n-gz"]/text()').extract_first()
        up_fans_count = response.xpath('//*[@id="n-fs"]/text()').extract_first()
        up_play_count = response.xpath('//*[@id="n-bf"]/text()').extract_first()


        # res = json.loads(response.body.decode('utf-8'))

        # up_name = res['h-name']
        # up_certification = res['h-ceritification']
        print("title---------------------" + str(title))
        print("column---------------------" + str(column))
        print("publish_date---------------------" + str(publish_date))
        print("ranking---------------------" + str(ranking))
        print("play_count---------------------" + str(play_count))
        print("danmu_count---------------------" + str(danmu_count))
        print("like_count---------------------" + str(like_count))
        print("corn_count---------------------" + str(corn_count))
        print("text_introduce---------------------" + str(text_introduce))
        print("keywords_tag---------------------" + str(keywords_tag))
        print("up_comments---------------------" + str(up_comments))
        print("up_name---------------------" + str(up_name))
        print("up_certification---------------------" + str(up_certification))
        print("up_introduction---------------------" + str(up_introduction))
        print("up_focus_count---------------------" + str(up_focus_count))
        print("up_fans_count---------------------" + str(up_fans_count))
        print("up_play_count---------------------" + str(up_play_count))

        item['title'] = title
        item['column'] = column
        item['publish_date'] = publish_date
        item['ranking'] = ranking
        item['play_count'] = play_count
        item['danmu_count'] = danmu_count
        item['like_count'] = like_count
        item['corn_count'] = corn_count
        item['text_introduce'] = text_introduce
        item['keywords_tag'] = keywords_tag
        item['up_comments'] = up_comments

        item['up_name'] = up_name
        item['up_certification'] = up_certification
        item['up_introduction'] = up_introduction
        item['up_focus_count'] = up_focus_count
        item['up_fans_count'] = up_fans_count
        item['up_play_count'] = up_play_count
        yield item
        print('--------------------up_page_parse end-------------------')





