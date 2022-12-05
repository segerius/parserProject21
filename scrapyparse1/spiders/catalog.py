import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['catalog.onliner.by']
    start_urls = ['http://catalog.onliner.by/']
    pages_count = 44

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://catalog.onliner.by/videocard?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.schema-product_pard .js-product-title-link::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        item = {
            'title': response.css('.product.full_name::text').extract_first('').strip(),
        }
        yield item
#123