from USDotWebScraper import USDotWebScraper

class Main:
    def __init__(self) -> None:
        pass
    
    def run(self):
        us_dot_scraper = USDotWebScraper()
        test_page = us_dot_scraper.request_web_page("https://ai.fmcsa.dot.gov/SMS/Carrier/21800/CarrierRegistration.aspx")
        print("testing")
        # print(test_page.text)
        
        result = us_dot_scraper.parse_web_page(test_page,[])
    
    
    
if __name__ == "__main__":
    main = Main()
    print("scraper")
    main.run()
    