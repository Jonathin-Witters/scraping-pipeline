from pathlib import Path

import scrapy

class DeStandaardSpider(scrapy.Spider):
    name = "DeStandaard"
    start_urls = [
        "https://www.standaard.be"
    ]

    custom_settings = {
        'FEEDS': {
            'data/de_standaard.json': {
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
        for teaser in response.css("article"):

            premium_marker = (
                    teaser.css('[class*="teaser-premium"]').get() or
                    teaser.css('[class*="title__premium"]').get() or
                    teaser.css("span::text").re_first(r"Premium")
            )

            if premium_marker:
                continue # skip articles behind paywall

            if teaser.css('[class*="TeaserEditorial_teaser-editorial"]'):
                continue  # skip live blogs

            article_url = teaser.css('a::attr(href)').get()
            yield response.follow(article_url, self.parse_article)

        page = response.url.split("/")[-2] or "index"
        filename = f"deStandaard-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

    def parse_article(self, response):
        yield {
            "title": response.css('[class^="story-headline_storyHeadline"] h1::text').get(),
            "date": response.css('time::attr(datetime)').get(),
            "author": response.css('p[data-testid="author-name"]::text').get(),
            "url": response.url,
            "source": "De Standaard",
            "first_lines": response.css('h2[data-testid="article-intro"]::text').get(),
            "thumbnail": response.css('img::attr(src)').get(),
            "tags": response.css('a[data-testid="article-tag"]::text').getall(),
            "content": "TODO",
        }

    def is_paywalled(self, response) -> bool:
        return bool(response.css('body.style_disable-scroll-popup__DWrnH'))
