import scrapy
from scrapy.spiders import Rule
from scrapy_selenium import SeleniumRequest


class CrawlerSpider(scrapy.Spider):
    name = "crawler"

    def __init__(self, *args, **kwargs):
        self.url = kwargs.get("url")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
        CrawlerSpider.rules = [
            Rule(SeleniumRequest(url=self.url, callback=self.parse, headers=headers, wait_time=5))
        ]

        super.__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        return response
