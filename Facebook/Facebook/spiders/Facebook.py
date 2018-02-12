# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request


class Facebook(scrapy.Spider):
    name = "facebook"

    def start_requests(self):
        url = 'http://facebook.com'
        method = 'GET'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        yield Request(url, callback=self.parse, method=method, headers=headers)

    def parse(self, response):
        for title in response.css('body'):
            yield {'text': title.css('form#login_form').extract()}
