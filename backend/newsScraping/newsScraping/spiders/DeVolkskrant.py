from pathlib import Path

import scrapy

# Data Model:

# Document {
# title: string
# date: date
# author: string
# url: url
# source: string
# first_lines: string
# thumbnail: img (/url)
# tags: string[]
# content: string
# } 


class DeVolkskrantSpider(scrapy.Spider):
    name = "devolkskrant"
    start_urls = [
        "https://www.volkskrant.nl/nieuws"
    ]

    custom_settings = {
        'FEEDS': {
            'data/devolkskrant.json': {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf8'
            }
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for teaser in response.css('li[class="teaser-list-item"]'):
            if teaser.css('[data-content-access-category="FREE"]').get():
                article_url = teaser.css('a::attr(href)').get()
                yield response.follow(article_url, self.parse_article)

        page = response.url.split("/")[-2] or "index"
        filename = f"devolkskrant-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

    def parse_article(self, response):
        yield {
            "title": response.css('h1[data-test-id="article-title"]::text').get(),
            "date": response.css('time::attr(datetime)').get(),
            "author": response.css('a[rel="author"]::text').get(),
            "url": response.url,
            "source": "De Volkskrant",
            "first_lines": response.css('p[data-test-id="header-intro"]::text').getall()[0],
            "thumbnail": response.css('img::attr(src)').get(),
            "tags": response.css('span[data-test-id="article-label"]::text').getall(),
            "content": response.css('p::text').getall(),
        }
