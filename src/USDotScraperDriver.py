from USDotWebScraper import USDotWebScraper
import argparse
import csv
import json

class USDotScraperDriver:
    def __init__(self) -> None:
        pass
    
    def run(self, filename):
        us_dot_scraper = USDotWebScraper()
        cargo_store = []
        attribute_store = []
        failed_entries = []
        
        with open(filename, newline='') as inputfile:
            dot_num_reader = csv.DictReader(inputfile)
            for row in dot_num_reader:
                dot_num = row["U.S. DOT#:"]
                url = "https://ai.fmcsa.dot.gov/SMS/Carrier/"+ dot_num +"/CarrierRegistration.aspx"
                print(url)
                web_page = us_dot_scraper.request_web_page(url)
                print(web_page)
                # Ideally we'd check if the error code is 200 before proceeding. The website returns 
                # 200 even is the dot number is wrong.
                attribute_dict, cargo_dict = us_dot_scraper.parse_web_page(web_page)
                if attribute_dict == None:
                    failed_entries.append(dot_num)
                    continue
                cargo_store.append(cargo_dict)
                attribute_store.append(attribute_dict)
        cargo_file_name = filename[:-4] + "cargo.json"
        attribute_file_name = filename[:-4] + "attribute.csv"
        failed_entries_file = filename[:-4] + "failed.csv"
        # storing registration info in 1 file
        with open(attribute_file_name, 'w', newline='') as csvfile:
            headers = us_dot_scraper.get_headers()
            attribute_file_writer = csv.DictWriter(csvfile, fieldnames=headers)
            
            
            attribute_file_writer.writeheader()
            for item in attribute_store:
                key_dot = list(item.keys())[0]
                item[key_dot]["U.S. DOT#:"] = key_dot
                attribute_file_writer.writerow(item[key_dot])
        # storing cargo info in another. csv format isn't particularly the best format for 1 to many relationships.
        # 1 truck may have 10 items while another has 20.  
        with open(cargo_file_name, "w") as cargo_json_file:
            formatted_json = json.dumps(cargo_store, indent=2)
            cargo_json_file.write(formatted_json)
            
        with open(failed_entries_file, 'w', newline='') as failed_file:
            headers = ["Failed dot #"]
            failed_file_writer = csv.DictWriter(failed_file, fieldnames=headers)
            failed_file_writer.writeheader()
            for entry in failed_entries:
                failed_file_writer.writerow({"Failed dot #":entry})
    
    
    
if __name__ == "__main__":
    main = USDotScraperDriver()
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--file", help="input file")
    argParser.add_argument("-o", "--outputfile", help="input file")
    args = argParser.parse_args()
    main.run(args.file)
    