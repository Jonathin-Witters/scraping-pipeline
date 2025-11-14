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


class VrtNwsSpider(scrapy.Spider):
    name = "vrtNws"
    start_urls = [
        "https://www.vrt.be/vrtnws/en/"
    ]

    custom_settings = {
        'FEEDS': {
            'data/vrt_nws.json': {
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
        for teaser in response.css('div[class~="@container/teaser"]'):
            article_url = teaser.css('a::attr(href)').get()
            yield response.follow(article_url, self.parse_article)

        page = response.url.split("/")[-2] or "index"
        filename = f"vrtNws-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

    def parse_article(self, response):
        yield {
            "title": response.css('div[data-sentry-component="ArticleHeading"] h1::text').get(),
            "date": response.css('time::attr(datetime)').get(),
            "author": response.css('div[data-sentry-component="ArticleAuthorSimple"] a::text').get(),
            "url": response.url,
            "source": "VRT NWS",
            "first_lines": response.css('div.text-on-surface-default.order-5.font-semibold.prose-article-body-r p::text').get(),
            "thumbnail": response.css('img::attr(src)').get(),
            "tags": response.css('div[data-sentry-component="DetailMore"] span::text').getall(),
            "content": response.css('div[data-sentry-component="ArticleText"] p::text').getall(),
        }