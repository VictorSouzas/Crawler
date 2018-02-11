# -*- coding: utf-8 -*-

import scrapy


class FacebookSpider(scrapy.Spider):
    name = "facebook"
    start_urls = [
        'http://facebook.com/',
    ]

    def parse(self, response):
        for quote in response.css('table'):
            yield {
                'text': table.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)