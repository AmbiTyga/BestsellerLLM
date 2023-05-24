import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Spider
from scrapy.linkextractors import LinkExtractor

class MyItem(scrapy.Item):
    text = scrapy.Field()
    
class AmazonSpider(scrapy.Spider):
    name = 'amzSpider'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    allowed_domains = ['amazon.in']
    start_urls = ["https://www.amazon.in/gp/bestsellers/"]

    def parse(self, response):
        all_departments = [
            "https://www.amazon.in" + i 
            for i in response.css('div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz div a::attr(href)').getall()
            ]
        
        for department_url in all_departments:
            yield response.follow(department_url, callback = self.parse_department, headers={'User-Agent': self.user_agent})
        
    def parse_department(self, response):
        products = [
            "https://www.amazon.in" + i 
            for i in response.css('div.p13n-sc-uncoverable-faceout a:nth-child(2)::attr(href)').getall()
            ]

        for product_url in products:
            yield response.follow(product_url, callback = self.parse_page, headers={'User-Agent': self.user_agent})
    
    def parse_page(self, response):
        title = response.css("h1#title span#productTitle::text").get()
        rating = response.css("span#acrPopover span.a-size-base.a-color-base::text").get()
        ratersCount = response.css("span#acrCustomerReviewText::text").get()
        if title is not None and rating is not None and ratersCount is not None:
            specification = "\n".join([x.strip() if x is not None else "" for x in response.css("ul.a-unordered-list.a-vertical.a-spacing-mini li span::text").getall()])
            data = f"Product: {title.strip()}\nRating: {rating.strip()}\nNumber of consumers who rated the product: {ratersCount.strip()}\nDescription: {specification}"
            yield MyItem(text=data)