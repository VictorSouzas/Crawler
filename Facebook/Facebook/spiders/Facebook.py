# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from scrapy.selector import Selector
import time


class Facebook(scrapy.Spider):
    name = "facebook"

    def start_requests(self):
        url = 'http://facebook.com'
        method = 'GET'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        yield Request(url, callback=self.parse, method=method, headers=headers)

    def parse(self, response):
        # yield {'text': content.xpath('//form[@id="login_form"]').extract_first() }
        binary = FirefoxBinary('/usr/lib/firefox/firefox')
        self.driver = webdriver.Firefox(firefox_binary=binary)
        self.driver.get(response.url)
        time.sleep(10)
        content = Selector(text=self.driver.page_source)
        yield { 'Html': content.xpath('//form[@id="login_form"]').xpath('//table').extract() }
