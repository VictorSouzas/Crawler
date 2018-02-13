# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.http import TextResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class Facebook(scrapy.Spider):
    name = "facebook"

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.binary = FirefoxBinary('/usr/lib/firefox/firefox')

        self.url = "http://facebook.com"

    def login(self, response):
        self.driver = webdriver.Firefox(firefox_binary=self.binary)
        self.driver.get(response.url)
        response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        yield {"text": response.selector.xpath('//form')}

    def start_requests(self):
        method = 'GET'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        yield Request(url=self.url, callback=self.login, method=method, headers=headers)

    def parse(self, response):
        # yield {'text': content.xpath('//form[@id="login_form"]').extract_first() }
        # binary = FirefoxBinary('/usr/lib/firefox/firefox')
        # self.driver = webdriver.Firefox(firefox_binary=binary)
        # self.driver.get(response.url)
        # time.sleep(10)
        # content = Selector(text=self.driver.page_source)
        # yield {'Html': content.xpath('//form[@id="login_form"]').xpath('//table').extract()}
        pass
