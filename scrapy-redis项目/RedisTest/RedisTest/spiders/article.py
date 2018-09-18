from scrapy_redis.spiders import RedisSpider
from ..items import RedistestItem


class ArticleSpider(RedisSpider):
    name = 'article'
    redis_key = "bole_urls"

    def parse(self, response):
        article_list = response.xpath("//div[@class='post floated-thumb']")
        for article in article_list:
            item = RedistestItem()
            item['title'] = article.xpath("div[@class='post-meta']/p[1]/a/@title").extract_first()
            yield item