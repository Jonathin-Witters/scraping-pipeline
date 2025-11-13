from bs4 import BeautifulSoup
from datetime import date
from Article import ArticleParser, Document

class DeStandaardArticleParser(ArticleParser):
    def parse(self, soup: BeautifulSoup) -> Document:
        article = soup.find_all("article")[0]

        return Document(
            title=self.parseTitle(article),
            author="TODO",
            date=self.parseDate(article),
            url="test",
            source="DeStandaard",
            first_lines=self.parseIntro(article),
            thumbnail=self.parseImageUrl(article),
            tags=[],
            content=self.parseContent(article),
        )

    def parseTitle(self, article) -> str:
        headerGroup = article.find_all("hgroup")[0]
        title = headerGroup.find_all("h1")[0]
        return title.text

    def parseDate(self, article) -> date:
        headerGroup = article.find_all("hgroup")[0]
        time = headerGroup.find_all("time")[0]
        return time["datetime"]

    def parseIntro(self, article) -> str:
        headerGroup = article.find_all("hgroup")[0]
        h2 = headerGroup.find_all("h2")[0]
        return h2.text

    def parseContent(self, article) -> str:
        content_section = article.find_all("section")[0]
        paragraphs = content_section.find_all("p")
        text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return text

    def parseImageUrl(self, article) -> str:
        img = article.find_all("img")[0]
        if img and img.has_attr("src"):
            return img["src"]
        return ""

    # def parseTags(self, article) -> List[str]:

    # def parseAuthor(self, article) -> str:
