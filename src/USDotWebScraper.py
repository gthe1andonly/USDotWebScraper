import requests
# bs4 vs scrapy
# Some quick research revealed that scapy does not properly support javascript. 
# If the website is to evolve and include more javascript, it will be easier to modify bs4 code to support those changes.
# Scrapy can be used to download, edit and save web data. Some of this seems currently out of scope and it is better practice 
# to engineer with the current requirements than those that have not been defined yet.
# One major advantage of scrapy is that it allows us to throttle the scrapping speed. Aknowledging that this would be
# ideal for our use case as the website frequently goes down. We can easily get around this by writing a cron job that executes 
# at more opportune times.
from bs4 import BeautifulSoup 

class USDotWebScraper:
    
    def __init__(self) -> None:
        # I initially wanted this to be a set. I am changing it to a list because 
        # I want the us dot # to be the first value.
        self.attribute_set = ["U.S. DOT#:"]
    
    def request_web_page(self, url) -> requests.Response:
        web_page = requests.get(url)
        return web_page
    
    def parse_web_page (self, web_page) -> tuple[dict, dict]:
        # per some online documentation, content help avoid extra problems with the parser as opposed to the .text of the page
        page_soup = BeautifulSoup(web_page.content, "html.parser")
        
        # The relevant info should be found under this box until otherwise noted
        result = page_soup.find(id="regBox")
        # assuming each carrier number is a 5 digit number. We can search using regex. There may be 
        # better ways to search for this, but for the sake of speed, I am searching with regex.
        # for dat in dat_elements:
        #     carrier_num = re.match("(?<!\d)\d{5}(?!\d)", dat.text)
        #     if carrier_num is not None:
        #         num_arr.append(carrier_num)
        # Further inspection of example data revealed this assumption was incorrect.
        
        # Incorrect entries will not have a registration box.  
        if result == None:
            return None, None
        cargo_list = result.find_all("ul", {"class": "cargo"})
        cleaned_cargo_list = []
        for cargo in cargo_list:
            cleaned_cargo_list.extend(cargo.text.splitlines())
        cleaned_cargo_list = [item for item in cleaned_cargo_list if len(item) > 0]
        # we're having some items containing mutiple items in them. This can be cleaned later
            
        attributes_list = result.find("ul",{"class": "col1"})
        attributes_list.extend(result.find("ul",{"class": "col2"}))
        
        attribute_text = []
        for attribute in attributes_list:
            attribute_temp = attribute.get_text().splitlines()
            attribute_temp = [atr.strip().upper() for atr in attribute_temp if len(atr.strip()) > 0]
            if len(attribute_temp) > 0:
                attribute_text.append(attribute_temp)
            
        
        for attribute in attribute_text:
            if attribute[0] not in self.attribute_set:
                self.attribute_set.append(attribute[0]) 
    
        us_dot_num, attribute_dictionary = self.construct_carrier_dict(attribute_text)
        
        return attribute_dictionary, {us_dot_num : cleaned_cargo_list}
    
    def construct_carrier_dict(self, attribute_list) -> tuple[str, dict]:
        # There are some issues with the parser not pulling info in the best format. For the sake of speed,
        # I am continuing as is. An example is address. This can be modified at a later time to properly show the info
        carrier_dictionary = {}
        us_dot_num = ""
        print("atr_list: ", attribute_list)
        for item in attribute_list:
            if item[0] == "U.S. DOT#:":
                us_dot_num = item[1]
            elif item[0] == "ADDRESS:" and len(item) > 2:
                # This can be cleaned at a later time. 
                carrier_dictionary['MAILING_STREET'] = item[1]
                self.attribute_set.append('MAILING_STREET')
                carrier_dictionary['MAILING_STATE_ZIP'] = item[2] 
                self.attribute_set.append('MAILING_STATE_ZIP')
                carrier_dictionary['PHY_STREET'] = item[1]
                self.attribute_set.append('PHY_STREET')
                carrier_dictionary['PHY_STATE_ZIP'] = item[2]
                self.attribute_set.append('PHY_STATE_ZIP')
            elif len(item) == 1:
                carrier_dictionary[item[0]] = ""
            else:
                carrier_dictionary[item[0]] = item[1]
                
        return us_dot_num, {us_dot_num : carrier_dictionary}
        
    def get_headers(self):
        return list(self.attribute_set)
    
        
    
     