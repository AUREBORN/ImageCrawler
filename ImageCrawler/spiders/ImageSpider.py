'''
#version: 1.0
#author: Sky Liu
'''

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
from scrapy.spiders import Spider
from selenium import webdriver
from scrapy.selector import Selector
from ImageCrawler.items import ImagecrawlerItem
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ImageSpider(Spider):
    name = 'imagespider'
    allowed_domins = ["vogue.com"]
    start_urls = [
        'http://www.vogue.com/fashion-shows/fall-2016-couture',
    ]

    def __init__(self):
        Spider.__init__(self)
        self.browser = webdriver.Chrome('/Users/liulizhe/Desktop/python_file/chromedriver')

    def __del__(self):
        self.browser.close()

    def parse_collection_url(self, response):
        self.browser.get(response.url)


    def parse_image(self, response):
        self.browser.get(response.url)

        # get collection label
        collection = self.browser.find_element(By.XPATH, '//li[@data-reactid="64"]')

        actions = ActionChains(self.browser)
        actions.click(collection)
        actions.perform()

        sel = Selector(text = self.browser.page_source)
        mycollection = sel.xpath("//span[@class='article-content--title']/text()").extract()
        print '------------------------------'
        print mycollection
        print '------------------------------'
        new_image_urls = []
        image_urls = sel.xpath("//img[@class='grid-item--image']/@srcset").extract()

        for image_url in image_urls:
            image_url = image_url.replace('w_195', 'w_1520')
            new_image_urls.append(image_url)

        item = ImagecrawlerItem()
        item['image_urls'] = new_image_urls
        item['name'] = mycollection

        yield item




    def parse(self, response):

        # start browser
        '''
        self.browser.get(response.url)
        season = self.browser.find_element(By.XPATH, '//span[@data-reactid="40"]')

        actions = ActionChains(self.browser)
        actions.click(season)
        actions.perform()

        # loading time interval
        self.browser.implicitly_wait(10)
        print self.browser.page_source
        '''

        sel = Selector(response)

        topshows_urls = sel.xpath("//div[@class='carousel--item match-height']/a/@href").extract()
        for topshow_url in topshows_urls:
            topshow_url = 'http://www.vogue.com' + topshow_url
            yield scrapy.Request(topshow_url, callback=self.parse_image)
