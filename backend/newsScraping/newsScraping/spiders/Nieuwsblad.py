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


class NieuwsbladSpider(scrapy.Spider):
    name = "nieuwsblad"
    start_urls = [
        "https://www.nieuwsblad.be"
    ]

    custom_settings = {
        'FEEDS': {
            'data/nieuwsblad.json': {
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
        for teaser in response.css('article'):
            article_url = teaser.css('a::attr(href)').get()
            yield response.follow(article_url, self.parse_article)

        page = response.url.split("/")[-2] or "index"
        filename = f"nieuwsblad-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

    def parse_article(self, response):
        yield {
            "title": response.css('h1[data-testid="article-headline"]::text').get(),
            "date": response.css('time::attr(datetime)').get(),
            "author": response.css('p[data-testid="author-name"]::text').get(),
            "url": response.url,
            "source": "Nieuwsblad",
            "first_lines": response.css('h2[data-testid="article-intro"]::text').get(),
            "thumbnail": response.css('img::attr(srcset)').get().split(',')[0],
            "tags": response.css('a[data-testid="article-tag"]::text').getall(),
            "content": response.css('section[data-testid="article-body"] p::text').getall(),
        }
        
        