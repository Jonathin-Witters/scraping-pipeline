from bs4 import BeautifulSoup
from parsers.deStandaard import DeStandaardArticleParser
import requests

# Need to spoof the website by acting as a user. Otherwise the request is rejected.
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

# Test with 1 article
url = "https://www.standaard.be/politiek/vlaamse-regering-vindt-compromis-zowel-vlaams-nationalistische-als-linkse-organisaties-verliezen-subsidies/104395940.html"
response = requests.get(url, headers=headers)
soup_article = BeautifulSoup(response.text, "html.parser")

parser = DeStandaardArticleParser()
parsed = parser.parse(soup_article)