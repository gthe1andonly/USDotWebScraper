## USDOT web scraper 

## Requirements:
#### Scrape Carrier Registration Details page for #### each operator in Motor Carrier Census Information file.
#### Need vehilcle type breakout table as well as list of cargo carried

#### Accessing the carrier regisration details: 
#### https://ai.fmcsa.dot.gov/SMS/Carrier/[DOT_NUMBER]/CarrierRegistration.aspx 
#### DOT number is a unique identifier for each carrier

#### In order to account for the usdot website going down, I want to implement a mechanism to check for items already
#### scraped. Before scraping for an item, the package should first check if it exists in our csv file unless 
#### explicitly told to override the previous entry. 
#### A sleep -> retry strategy can be used to account for a transient issue like loss of network connection.