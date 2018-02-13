# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import TextResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import getpass
import time


class Facebook(scrapy.Spider):
    name = "facebook"

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.password = getpass.getpass(prompt="Password: ")
        self.binary = FirefoxBinary('/usr/lib/firefox/firefox')
        self.driver = webdriver.Firefox(firefox_binary=self.binary)
        self.url = "http://facebook.com"

    def login(self):
        self.driver.get(self.url)
        element_email = self.driver.find_element_by_xpath('//form[@id="login_form"]//input[@name="email"]')
        element_pass = self.driver.find_element_by_xpath('//form[@id="login_form"]//input[@name="pass"]')
        element_button = self.driver.find_element_by_xpath('//form[@id="login_form"]//input[@type="submit"]')
        login = "victor_souzas@yahoo.com.br"
        element_email.send_keys(login)
        element_pass.send_keys(self.password)
        element_button.click()
        time.sleep(2)

    def go_friends_page(self):
        element_link = self.driver.find_element_by_xpath('//div[@data-click="profile_icon"]//a')
        element_link.click()
        time.sleep(2)
        element_link = self.driver.find_element_by_xpath('//li//a[@data-tab-key="friends"]')
        element_link.click()
        time.sleep(2)
        # response = HtmlXPathSelector(self.driver.page_source)

    def load_friends_page(self):
        size = {"height": 1}
        last_size = {"height": 0}
        while size["height"] > last_size["height"]:
            l = self.driver.find_element_by_xpath('//div[@id="pagelet_timeline_medley_friends"]')
            last_size = l.size
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            s = self.driver.find_element_by_xpath('//div[@id="pagelet_timeline_medley_friends"]')
            size = s.size

    def parser(self):
        pass

    def start_requests(self):
        yield self.login()
        yield self.go_friends_page()
        yield self.load_friends_page()
        yield self.parser()
