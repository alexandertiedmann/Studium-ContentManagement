# scraper.py
# Aufgabe a)
from scrapy.spider import BaseSpider
from scrapy import Request


class DatascraperSpider(BaseSpider):
    name = "dataScraper"
    allowed_domains = ["htw-berlin.de"]
    start_urls = [
        'http://people.f4.htw-berlin.de/~zhangg/pages/teaching/pages/d01.html',
        'http://people.f4.htw-berlin.de/~zhangg/pages/teaching/pages/d06.html',
        'http://people.f4.htw-berlin.de/~zhangg/pages/teaching/pages/d08.html'
    ]
    crawled = []

    def start_request(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")
        page = page[len(page) - 1]
        self.crawled.append(page)
        filename = '%s' % page
        with open('' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        for href in response.css('a::attr(href)'):
            if href not in self.crawled:
                yield response.follow(href, self.parse)
