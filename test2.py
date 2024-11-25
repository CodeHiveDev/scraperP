import scrapy
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

# Configuración para Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

class SearchSpider(scrapy.Spider):
    name = "search_spider"
    allowed_domains = ["example.com"]  # Cambia esto al dominio que deseas rastrear
    start_urls = ["https://example.com"]  # URL inicial

    # Configura el User-Agent como Googlebot
    custom_settings = {
        'USER_AGENT': 'Googlebot/2.1 (+http://www.google.com/bot.html)'
    }

    def parse(self, response):
        # Analiza el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrae el título y el contenido
        title = soup.title.string if soup.title else "No Title"
        text = soup.get_text()

        # Indexa en Elasticsearch
        doc = {
            "url": response.url,
            "title": title,
            "content": text
        }

        print(doc)
        #es.index(index="web_index", body=doc)

        # Encuentra enlaces en la página
        for link in soup.find_all("a", href=True):
            url = response.urljoin(link['href'])
            yield scrapy.Request(url, callback=self.parse)
