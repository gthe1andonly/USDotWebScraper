import requests
# bs4 vs scrapy
from bs4 import BeautifulSoup 

class USDotWebScraper:
    
    def __init__(self) -> None:
        self.default_id_list = {"id":"regBox", "class": "cargo"}
    
    def request_web_page(self, url) -> requests.Response:
        web_page = requests.get(url)
        return web_page
    
    def parse_web_page (self, web_page, element_id_list) -> list[str]:
        # per some online documentation, content help avoid extra problems with the parser as opposed to the .text of the page
        page_soup = BeautifulSoup(web_page.content, "html.parser")
        result_items = []
        if len(element_id_list) == 0:
            element_id_list = self.default_id_list
        
        
        result =page_soup.find(id="regBox")
        print(result.prettify())
        return result_items
        
    
     