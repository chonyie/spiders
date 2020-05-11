from scrapy import cmdline
# cmdline.execute(['scrapy','crawl','zhihu'])
cmdline.execute('scrapy crawl zhihu'.split())