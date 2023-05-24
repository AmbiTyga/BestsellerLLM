import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Spider
from scrapy.linkextractors import LinkExtractor

class MyItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    ratersCount = scrapy.Field()
    info = scrapy.Field()

class AmazonSpider(scrapy.Spider):
    name = 'amzSpider'
    allowed_domains = ['amazon.in']
    start_urls = ["https://www.amazon.in/gp/bestsellers/"]

    def parse(self, response):
        all_departments = [
            "https://www.amazon.in" + i 
            for i in response.css('div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz div a::attr(href)').getall()
            ]
        
        for department_url in all_departments:
            yield response.follow(department_url, callback = self.parse_department)
        
    def parse_department(self, response):
        products = [
            "https://www.amazon.in" + i 
            for i in response.css('div.p13n-sc-uncoverable-faceout a:nth-child(2)::attr(href)').getall()
            ]

        for product_url in products:
            yield response.follow(product_url, callback = self.parse_page)
    
    def parse_page(self, response):
        title = response.css("h1#title span#productTitle::text").get().strip()
        rating = response.css("span#acrPopover span.a-size-base.a-color-base::text").get().strip()
        ratersCount = response.css("span#acrCustomerReviewText::text").get().strip()
        specification = [x.strip() for x in response.css("ul.a-unordered-list.a-vertical.a-spacing-mini li span::text").getall()]

        yield MyItem(title = title, rating = rating, ratersCount = ratersCount, info = specification)