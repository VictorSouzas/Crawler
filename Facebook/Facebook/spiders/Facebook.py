# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import TextResponse
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import getpass


class Facebook(scrapy.Spider):
    name = "facebook"

    def __init__(self):
        scrapy.Spider.__init__(self)

    def start_requests(self):
        yield Request("http://facebook.com.br", callback=self.parse)

    def parse(self, response):
        name = response.xpath('//div[@class="fsl fwb fcb"]//a/text()').extract()
        url =  response.xpath('//div[@class="fsl fwb fcb"]//a/@href').extract()
        dic = {}
        for key, value in zip(name, url):
            dic[key] = value
        yield dic 
                  
    
