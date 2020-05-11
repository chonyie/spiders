# -*- coding: utf-8 -*-
'''
    全站爬虫 从马化腾开始采集全站信息
'''
import json,re
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/api/v4/members/ponyma/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=40&limit=20']

    def parse(self, response):
        # 提取数据
        jsonData = json.loads(response.text)
        if jsonData.get('data'):
            for dat in jsonData['data']:
                # 打印出数据 这个里面有url_token数据
                print(dat)
                url_token = dat['url_token']
                # 马化腾粉丝的粉丝的网址
                url_follers = f'https://www.zhihu.com/api/v4/members/{url_token}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20'
                yield dat
                # 粉丝的粉丝的数据
                yield scrapy.Request(url_follers, callback=self.parse)

        # 翻页
        if jsonData.get('paging'):
            is_end = jsonData['paging']['is_end']
            next_page = jsonData['paging']['next']
            next_url = re.sub('members', 'api/v4/members', next_page)
            print(next_url)
            if not is_end:
                yield scrapy.Request(next_url,callback=self.parse)