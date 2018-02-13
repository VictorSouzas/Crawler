# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

class FacebookSpiderMiddleware(object):
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


class FacebookDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        request.meta['driver'] = self.driver  # to access driver from response
        self.requests()
        body = to_bytes(self.driver.page_source)  # body must be of type bytes 
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)


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
        self.url = "http://www.facebook.com"
        self.binary = FirefoxBinary('/usr/lib/firefox/firefox')
        self.driver = webdriver.Firefox(firefox_binary=self.binary)

    def spider_closed(self, spider):
        self.driver.close()

    def login(self):
        self.driver.get(self.url)
        element_email = self.driver.find_element_by_xpath('//form[@id="login_form"]//input[@name="email"]')
        element_pass = self.driver.find_element_by_xpath('//form[@id="login_form"]//input[@name="pass"]')
        element_button = self.driver.find_element_by_xpath('//form[@id="login_form"]//input[@type="submit"]')
        login = ""
        password = ''
        element_email.send_keys(login)
        element_pass.send_keys(password)
        element_button.click()
        time.sleep(2)

    def go_friends_page(self):
        element_link = self.driver.find_element_by_xpath('//div[@data-click="profile_icon"]//a')
        element_link.click()
        time.sleep(2)
        element_link = self.driver.find_element_by_xpath('//li//a[@data-tab-key="friends"]')
        element_link.click()
        time.sleep(2)

    def load_friends_page(self):
        size = {"height": 1}
        last_size = {"height": 0}
        while size["height"] > last_size["height"]:
            load = self.driver.find_element_by_xpath('//div[@id="pagelet_timeline_medley_friends"]')
            last_size = load.size
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            s = self.driver.find_element_by_xpath('//div[@id="pagelet_timeline_medley_friends"]')
            size = s.size
        time.sleep(2)

    def requests(self):
        self.login()
        self.go_friends_page()
        self.load_friends_page()
