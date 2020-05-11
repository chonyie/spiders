# -*- coding: utf-8 -*-
import scrapy

from ..items import PictureItem


class VmgirlsSpider(scrapy.Spider):
    name = 'vmgirls'
    allowed_domains = ['vmgirls.com']

    start_urls = ['https://www.vmgirls.com/12985.html']

    # def start_requests(self):
    #     """重写 start_urls 规则"""
    #     yield scrapy.Request(url='https://www.vmgirls.com/special/%e5%b0%8f%e5%a7%90%e5%a7%90', callback=self.parse_url)

    def parse_url(self, response: scrapy.Selector):
        # 解析每个页面的下载网址
        img_urls = response.css('.media-content::attr(href)').extract()
        print(img_urls)
        for img_url in img_urls:
            yield scrapy.Request(url=img_url, callback=self.parse)

    def parse(self, response: scrapy.Selector):
        item = PictureItem()
        item['title'] = response.css('h1::text').extract_first()
        item['img_s'] = response.css('.post-content img::attr(data-src)').extract()
        print(item['img_s'])
        yield item
