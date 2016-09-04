# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

class ImagecrawlerPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url, meta={'item': item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('图片未下载好 %s' % image_paths)

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        imgae_guid = request.url.split('/')[-1]
        class_guid = item['name']
        return 'full/%s/%s' % (class_guid, imgae_guid)
