# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonLinesItemExporter

class ZhihuspiderItmePipeline(object):

    def __init__(self):
        self.f = open('zhihu.csv','wb')
        self.exportor = CsvItemExporter(self.f)
        self.exportor.start_exporting()

    def process_item(self, item, spider):
        self.exportor.export_item(item)
        return item

    def close_spider(self,spider):
        self.exportor.finish_exporting()
        self.f.close()


class ZhihuspiderPipeline(object):

    def __init__(self):
        self.f = open('zhihu1.csv')

    def open_spider(self,spider):
        pass

    def process_item(self, item, spider):
        self.f.write(str(item)+'\n')
        return item

    def close_spider(self,spider):
        self.f.close()
