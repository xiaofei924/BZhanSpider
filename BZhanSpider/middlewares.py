# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from twisted.conch.telnet import EC

"""
是和Scrapy的请求/响应处理相关联的框架。
中间件处理request和response

"""
class BzhanspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BzhanspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        print("-----------------------------BzhanspiderDownloaderMiddleware-----------------------------")
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware(object):
    def __init__(self,timeout=25):

        # 设置selenium不加载图片,固定写法
        chrome_opt = webdriver.ChromeOptions()
        prefs = {
                'profile.default_content_setting_values': {
                    'images': 2,  # 禁用图片的加载
                    # 'javascript': 2  # 禁用js，可能会导致通过js加载的互动数抓取失效
                }
            }
        # prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_opt.add_experimental_option('prefs', prefs)
        self.browser = webdriver.Chrome(chrome_options=chrome_opt)

        self.timeout = timeout
        # self.browser = webdriver.Firefox()
        # self.browser = webdriver.Chrome()
        # self.browser.minimize_window()
        self.browser.set_window_size(900, 900)
        # self.browser.implicitly_wait(20)
        # self.browser.set_page_load_timeout(25)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)


    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        """
        用ChromeDriver抓取页面
        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """

        # print('******ChromeDriver is Starting******')
        print('-------------------ChromeDriver is Starting---------------------------')
        try:
            self.browser.get(request.url)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        except TimeoutException as e:
            print('-------------------------请求超时------------------------')
            self.browser.execute_script('window.stop()')
            return HtmlResponse(url=request.url, body=self.browser.page_source, encoding="utf-8",
                            request=request, status=500)
        else:
            time.sleep(2)
            return HtmlResponse(url=request.url, body=self.browser.page_source, encoding="utf-8",
                        request=request,status=200)