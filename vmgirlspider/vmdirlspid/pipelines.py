# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class DownloadPicturePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['img_s']:
            yield scrapy.Request(image_url, meta={'filename': item['title']})

    def file_path(self, request, response=None, info=None):
        # 重命名，若不重写这函数，图片名为哈希
        # 提取url前面名称作为图片名。
        filename = request.meta.get('filename')
        image_guid = request.url.split('/')[-1]
        return os.path.join(filename, image_guid)

    def item_completed(self, results, item, info):
        print(results)
        print('*'*50)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] 文件存放的位置
        item['image_paths'] = image_paths
        return item
