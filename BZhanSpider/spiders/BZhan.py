# -*- coding: utf-8 -*-
import collections
import json
from builtins import print
import time

import scrapy
import self as self

from BZhanSpider.replybean import replybean
from BZhanSpider.items import BzhanspiderItem
from selenium import webdriver

from BZhanSpider.middlewares import SeleniumMiddleware
from urllib import request, parse

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

    start_url = input('请输入要抓取B站视频信息的网址, 按回车结束: \n')
    start_url_parse = parse.urlparse(start_url)
    start_url_path = start_url_parse.path
    start_urls = ['http://www.bilibili.com/video/av48323686/']

    # # https: // api.bilibili.com / x / web - interface / view?aid = 48465492
    # # start_urls = ['https://api.bilibili.com/x/web-interface/view?aid=48465492']#播放界面数据类型json\
    # page_data_url = 'http://www.bilibili.com/video/av48323686'#界面数据，无法获取数量
    # data_url = 'https://api.bilibili.com/x/web-interface/view?aid=48465492'#数据数量(弹幕、播放、点赞等)
    # url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=48465492'#数量json
    # comment_url = 'https://api.bilibili.com/x/v2/reply?callback=jQuery17202434448397650979_1554717195061&jsonp=jsonp&pn=2&type=1&oid=48465492&sort=0&_=1554718673887'
    # # start_urls = [start_url]
    # # video / av48323686
    # video_comment_url = 'https://api.bilibili.com/x/v2/reply?callback=jQuery17208525034767588849_1554860847400&jsonp=jsonp&pn=2&type=1&oid=48323686&sort=0&_=1554863787356'
    reply_comment_base_url = 'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn=%s&type=1&oid=%s&ps=10&root=%s'
    video_comment_url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=%s&type=1&oid=%s&sort=0'

    is_save = False
    reply_comment_type = -1
    # 视频评论
    video_comment = 0
    # 网友的回复
    net_friend_reply_comment = 1
    # up主的回复
    up_reply_comment = 2
    # 视频所有评论及回复，用于判断是否爬到所有评论及回复来保存数据
    total_reply_count = 0

    # 视频的id
    # 从start_url分解出来的path里面过滤
    start_url_path_split = start_url_path.split('/')[2]  # 分割后获取形如av48323686这个块
    oid = start_url_path_split[2:]  # 去掉av留下视频id
    print('---------------------视频id：' + oid + ' ------------------------')

    # 视频评论列表
    video_reply_map = collections.OrderedDict()
    # 评论下面的恢复列表，网友互动内容
    net_friend_reply_map = collections.OrderedDict()
    # 视频owner，up主的恢复列表
    up_reply_map = collections.OrderedDict()
    """
    start_urls主请求的回调，在里面解析数据并存储到items中去
    """

    def parse(self, response):  # 默认回调
        print('--------------parse start-----------------')
        # video_comment_url = 'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid=48323686&sort=0'

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
        favorite_count = response.xpath('/html/body/div[3]/div/div[1]/div[3]/div[1]/span[3]/text()').extract_first()
        text_introduce = response.xpath('/html/body/div[3]/div/div[1]/div[4]/div[1]/text()').extract()
        keywords_tag = response.xpath('/html/body/div[3]/div/div[1]/div[5]/ul//text()').extract()

        # comment_page_count = response.xpath('//div[@class="header-page paging-box"]/a[@class="tcd-number"]/text()').extract()[-1]
        # print(comment_page_count)
        #
        # if comment_page_count is not None:
        #     comment_page_count = int(comment_page_count)
        # else:
        #     comment_page_count = 0
        comment_page_count = 3
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

        # 评论先拿第一组数据测试
        up_comments = ''

        # yield item

        # 获取up主的网页url
        # 取指定第一个加[0], 否则会有type问题
        up_page_url = response.xpath('/html/body/div[3]/div/div[2]/div[1]/div[2]/div[1]/a[1]/@href').extract()[0]
        # 获取url绝对路径
        url = response.urljoin(up_page_url)
        print('-------------------' + str(up_page_url))
        print(url)

        # 视频owner的id，mid
        mid = ''

        # 请求评论的接口直接获取json数据进行解析
        if comment_page_count > 0:
            current_page = 1
            yield scrapy.Request(url=self.video_comment_url % (str(current_page), self.oid),
                                 callback=self.video_comment_parse,
                                 dont_filter=True, meta={'is_request_without_browser': True,
                                                         'comment_page_count': comment_page_count,
                                                         'current_page': current_page,
                                                         'mid': mid})

        # DEBUG: Filtered offsiterequest to因为Request中请求的URL和allowed_domains中定义的域名冲突，所以将Request中请求的URL过滤掉了，无法请求
        # 在Request请求参数中，设置dont_filter = True, Request中请求的URL将不通过allowed_domains过滤。
        yield scrapy.Request(url=url, callback=self.up_page_parse, dont_filter=True, meta={'title': title,
                                                                                           'column': column,
                                                                                           'publish_date': publish_date,
                                                                                           'ranking': ranking,
                                                                                           'play_count': play_count,
                                                                                           'danmu_count': danmu_count,
                                                                                           'like_count': like_count,
                                                                                           'corn_count': corn_count,
                                                                                           'favorite_count': favorite_count,
                                                                                           'text_introduce': text_introduce,
                                                                                           'keywords_tag': keywords_tag,
                                                                                           'up_comments': up_comments,

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

    def up_page_parse(self, response):
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
        favorite_count = response.meta['favorite_count']
        text_introduce = response.meta['text_introduce']
        keywords_tag = response.meta['keywords_tag']
        up_comments = response.meta['up_comments']

        up_name = response.xpath('//*[@id="h-name"]/text()').extract_first()
        up_introduction = response.xpath(
            '/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/h4/text()').extract_first()
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
        print("favorite_count---------------------" + str(favorite_count))
        print("text_introduce---------------------" + str(text_introduce))
        print("keywords_tag---------------------" + str(keywords_tag))
        print("up_comments---------------------" + str(up_comments))
        print("up_name---------------------" + str(up_name))
        print("up_introduction---------------------" + str(up_introduction))
        print("up_certification---------------------" + str(up_certification))
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
        item['favorite_count'] = favorite_count
        item['text_introduce'] = text_introduce
        item['keywords_tag'] = keywords_tag
        item['up_comments'] = up_comments

        item['up_name'] = up_name
        item['up_introduction'] = up_introduction
        item['up_certification'] = up_certification
        item['up_focus_count'] = up_focus_count
        item['up_fans_count'] = up_fans_count
        item['up_play_count'] = up_play_count
        # self.is_save = True

        # 回调item数据给pipelines
        yield item

        # #关闭浏览器
        # SeleniumMiddleware.__del__(self)

        print('--------------------up_page_parse end-------------------')

    """
    请求视频的评论，分为网友评论和up主评论分类存储
    """

    def video_comment_parse(self, response):
        print('-----------------------------video_comment_parse start-----------------------------')
        if response is None or response.body is None:
            return

        status = response.status
        if status != 200:
            print('request failed, status: ' + status)
            return
        # 回复评论的的url
        reply_comment_url = 'https://api.bilibili.com/x/v2/reply/reply?callback=jQuery17208938958981882081_1554882206023&jsonp=jsonp&pn=1&type=1&oid=48323686&ps=10&root=1503675439&=1554890310602'
        reply_comment_url = 'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn=1&type=1&oid=48323686&ps=10&root=1503675439'
        oid = ''
        up_mid = ''

        item = BzhanspiderItem()
        try:
            comment_page_count = 0
            current_page = -1
            if 'oid' in response.meta:
                oid = response.meta['oid']
            if 'up_mid' in response.meta:
                up_mid = response.meta['up_mid']
            resp = json.loads(response.body, encoding='utf-8')
            if 'data' not in resp:
                return
            data = resp['data']
            # 热门评论
            # hots = data['hots']
            replies = data['replies']
            page = data['page']
            upper = data['upper']
            """所有评论及回复只赋值一次，避免多次赋值导致爬取的和获取的acount数量不匹配导致不能存储"""
            if self.total_reply_count == 0 and page['acount'] > 0:
                self.total_reply_count = page['acount']
            print('------------评论及回复总数： ' + str(self.total_reply_count))
            current_page = page['num']
            item = BzhanspiderItem()

            comment_page_count = calculate_comment_page_count(page, True)
            hot_comments_url = 'https://api.bilibili.com/x/v2/reply?callback=&jsonp=jsonp&pn=1&type=1&oid=48323686&sort=2'

            for reply in replies:
                bean = get_reply_bean(reply, oid)
                # print(bean.to_string())
                # 视频评论保存
                if bean.get_mid() == upper['mid']:
                    self.up_reply_map[bean.get_rpid_str()] = bean
                else:
                    self.video_reply_map[bean.get_rpid_str()] = bean

                # 判断评论下面的回复是否存在，存在的话，继续遍历回复列表在comment_reply_parse里面处理所有回复
                comment_replies = reply['replies']
                if comment_replies is not None:
                    comment_reply_current_page = 1  # 默认请求第一页的的回复
                    yield scrapy.Request(url=self.reply_comment_base_url % (
                        str(comment_reply_current_page), self.oid, bean.get_rpid_str()),
                                         callback=self.comment_reply_parse,
                                         dont_filter=True,
                                         meta={'is_request_without_browser': True,
                                               'comment_reply_current_page': page,
                                               'root': bean.get_rpid_str()})

            # self.add_comments_to_map(hots)
            # self.add_comments_to_map(replies)
            page = current_page + 1
            if self.total_reply_count >= page > 0:
                yield scrapy.Request(url=self.video_comment_url % (str(page), self.oid),
                                     callback=self.video_comment_parse,
                                     dont_filter=True,
                                     meta={'is_request_without_browser': True,
                                           'comment_page_count': comment_page_count,
                                           'current_page': page})
            else:
                if Is_yield_comments_and_reply_to_pipelines(42, self.video_reply_map, self.net_friend_reply_map,
                                                            self.up_reply_map):
                    # if 'video_reply_map' in item:
                    item['video_reply_map'] = self.video_reply_map

                    # if 'up_reply_map' in item:
                    item['up_reply_map'] = self.up_reply_map

                    # if 'net_friend_reply_map' in item:
                    item['net_friend_reply_map'] = self.net_friend_reply_map
                    yield item
                # # print(self.video_reply_map)
                # # if 'video_reply_map' in item:
                # item['video_reply_map'] = self.video_reply_map
                # length = len(self.video_reply_map) + len(self.net_friend_reply_map) + len(self.up_reply_map)
                # if length >= 42:
                #     print('----------------------video_comment_parse------------------抓取完成， 返回评论 map 总和: ' + str(length) + '-------------------------------------------------------')
                #     yield item
        except TimeoutError as e:
            print('评论抓取失败, 失败原因' + str(e))
        print('-----------------------------video_comment_parse end-----------------------------')

    """
    处理评论下的回复，包括网友回复、up主回复，分类存储
    """

    def comment_reply_parse(self, response):
        print('-----------------------------comment_reply_parse start-----------------------------')
        try:
            oid = ''
            up_mid = ''
            root = ''  # 对应评论的rpid，用于url请求拿到指定rpid下面的回复列表
            comment_reply_current_page = -1  # 回复列表页数
            comment_reply_page_count = 0  # 回复列表当前页数

            item = BzhanspiderItem()
            if 'comment_reply_current_page' in response.meta:
                comment_reply_current_page = response.meta['comment_reply_current_page']
            if 'oid' in response.meta:
                oid = response.meta['oid']
            if 'up_mid' in response.meta:
                up_mid = response.meta['up_mid']
            if 'root' in response.meta:
                root = response.meta['root']

            resp = json.loads(response.body, encoding='utf-8')
            data = resp['data']
            replies = data['replies']
            page = data['page']
            upper = data['upper']

            comment_reply_current_page = page['num']
            comment_reply_page_count = calculate_comment_page_count(page, False)

            print('comment_reply_current_page' + str(comment_reply_current_page))
            print('comment_reply_page_count' + str(comment_reply_page_count))

            for reply in replies:
                bean = get_reply_bean(reply, oid)
                print(bean.to_string())

                # 评论下的回复进行保存，分网友和up主两类
                if bean.get_mid() == upper['mid']:
                    self.up_reply_map[bean.get_rpid_str()] = bean
                else:
                    self.net_friend_reply_map[bean.get_rpid_str()] = bean

                comment_replies = reply['replies']  # 评论下面的回复

                if comment_replies is not None:
                    page = 1
                    if comment_reply_page_count >= page > 0:
                        yield scrapy.Request(url=self.reply_comment_base_url % (str(page), oid, bean.get_root_str()),
                                             callback=self.comment_reply_parse,
                                             dont_filter=True,
                                             meta={'is_request_without_browser': True,
                                                   'root': bean.get_root_str()})
            length = len(self.video_reply_map) + len(self.net_friend_reply_map) + len(self.up_reply_map)

            page = comment_reply_page_count + 1
            if comment_reply_page_count >= page > 0:
                yield scrapy.Request(url=self.reply_comment_base_url % (str(page), oid, root),
                                     callback=self.comment_reply_parse,
                                     dont_filter=True,
                                     meta={'is_request_without_browser': True,
                                           'current_page': page,
                                           'root': root})
            else:
                if Is_yield_comments_and_reply_to_pipelines(42, self.video_reply_map, self.net_friend_reply_map,
                                                            self.up_reply_map):
                    # if 'video_reply_map' in item:
                    item['video_reply_map'] = self.video_reply_map

                    # if 'up_reply_map' in item:
                    item['up_reply_map'] = self.up_reply_map

                    # if 'net_friend_reply_map' in item:
                    item['net_friend_reply_map'] = self.net_friend_reply_map
                    yield item
                # if 'up_reply_map' in item:
                # item['up_reply_map'] = self.up_reply_map
                # item['net_friend_reply_map'] = self.net_friend_reply_map
                # # yield item
                # length = len(self.video_reply_map) + len(self.net_friend_reply_map) + len(self.up_reply_map)
                # if length >= 42:
                #     # print('--------------------------comment_reply_parse--------------抓取完成， 返回评论 map 总和: ' + str(length) + '-------------------------------------------------------')
                #     yield item
        except TimeoutError as e:
            print('评论下的回复抓取失败, 失败原因' + str(e))
        print('-----------------------------comment_reply_parse end-----------------------------')

    def add_comments_to_map(replies):
        if 0 >= len(replies):
            return

        for reply in replies:
            ctime = reply['ctime']
            time = time.strftime('%Y-%m-%d %H:%M:%S', reply['ctime'])
            content = reply['content']
            message = content['message']

        pass


"""
将数据存储javabean格式的数据结构并返回
"""


def get_reply_bean(reply, oid):
    # reply id
    rpid_str = reply['rpid_str']
    # 根评论的reply id，对应rpid_str
    root_str = reply['root_str']
    # 上一级评论(可能是回复的回复多层嵌套)
    parent_str = reply['parent_str']
    # reply 时间
    ctime = reply['ctime']
    # 时间戳转换为时间元祖
    time_tuples = time.localtime(ctime)
    # 再将时间元祖格式化
    date = time.strftime('%Y-%m-%d %H:%M:%S', time_tuples)
    # reply 楼层，第几楼
    floor = reply['floor']
    # reply 用户id，mid
    mid = reply['mid']
    member = reply['member']
    # reply 用户的用户名
    uname = member['uname']
    # 用户评论内容
    content = reply['content']
    message = content['message']
    # print('rpid_str: ' + str(rpid_str) + ', message: ' + str(message)
    #       + ', date: ' + str(date) + ', mid: ' + str(mid) + ', floor: ' + str(floor))

    return replybean(str(oid), str(rpid_str), str(date), str(floor), str(mid), str(uname),
                     str(message), str(root_str), str(parent_str))


"""
计算评论页数
"""


def calculate_comment_page_count(page, is_video_comment=True):
    acount = 0
    if 'acount' in page:
        acount = page['acount']  # 所有评论数(包括视频评论和评论下的回复)
    count = page['count']  # 总评论数
    num = page['num']  # 当前页是第几页
    size = page['size']  # 每一页的个数
    page_count = count // size
    if count % size > 0:
        page_count += 1
    if is_video_comment:
        print('评论: 所有评论数(包括视频评论和评论下的回复)：' + str(acount) + ', 视频评论数：' + str(count)
              + ', 总页数：' + str(page_count) + ', 当前第' + str(num) + '页， 每一页个数：' + str(size))
    else:
        print('回复: 当前视频评论下的回复数：' + str(count) + ', 总页数：' + str(page_count)
              + ', 当前第' + str(num) + '页， 每一页个数：' + str(size))
    return page_count


def Is_yield_comments_and_reply_to_pipelines(comment_reply_total_count, video_reply_map, net_friend_reply_map,
                                             up_reply_map):
    # print(self.video_reply_map)
    item = BzhanspiderItem()
    length = len(video_reply_map) + len(net_friend_reply_map) + len(up_reply_map)
    print('----------------------video_comment_parse------------------抓取完成， 返回评论 map 总和: ' + str(
        length) + '-------------------------------------------------------')

    if length >= comment_reply_total_count:
        return True
    else:
        return False


@staticmethod
def close(spider, reason):
    print('--------------------------------------------------BZhanSpider close----------------------------------------')
    yield spider.item
