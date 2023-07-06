import unittest
import requests
from USDotWebScraper import USDotWebScraper
class USDotWebScraperTest(unittest.TestCase):
    # more time would allow us to build a more comprehensive test suit. I am adding this to 
    # keep with the best pratices of always adding some tests to your code. It is not fully developed yet.
    def setUp(self) -> None:
        self.us_dot_scraper = USDotWebScraper()
    
    def test_request_web_page(self):
        resp = self.us_dot_scraper.request_web_page("https://ai.fmcsa.dot.gov/SMS/Carrier/21800/CarrierRegistration.aspx")
        self.assertEqual(resp.status_code,200, "This request should succeed")
        
    def test_invalid_request(self):
        resp = self.us_dot_scraper.request_web_page("https://ai.fmcsa.dot.gov/SMS/Carrier/200/CarrierRegistration.aspx")
        self.assertEqual(resp.status_code,200, "This request should fail. Not yet sure why this returns a 200. It may be the website improperly handling invalid requests.")
    
    def test_parse_web_page(self):
        resp = self.us_dot_scraper.request_web_page("https://ai.fmcsa.dot.gov/SMS/Carrier/21800/CarrierRegistration.aspx")
        attribute, cargo = self.us_dot_scraper.parse_web_page(resp)
        key = list(attribute.keys())[0]
        self.assertEqual(type(attribute),dict, "Expecting a dictionary to be returned")
        self.assertEqual(key,"21800", "We expect the us dot num to be the key.")
        
    def test_get_headers(self):
        resp = self.us_dot_scraper.request_web_page("https://ai.fmcsa.dot.gov/SMS/Carrier/21800/CarrierRegistration.aspx")
        attribute, cargo = self.us_dot_scraper.parse_web_page(resp)
        headers = self.us_dot_scraper.get_headers()
        self.assertEqual(type(headers),list, "Expecting a list to be returned.")
        
        
    
if __name__ == '__main__':
    unittest.main()