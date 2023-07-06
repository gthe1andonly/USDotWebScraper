## USDOT web scraper 

## Requirements:
#### Scrape Carrier Registration Details page for #### each operator in Motor Carrier Census Information file.
#### Need vehilcle type breakout table as well as list of cargo carried

#### Accessing the carrier regisration details: 
#### https://ai.fmcsa.dot.gov/SMS/Carrier/[DOT_NUMBER]/CarrierRegistration.aspx 
#### DOT number is a unique identifier for each carrier

### Running the code
#### 1. Download the project/repo
#### 2. Run the following command to install the necessary dependencies `pip install -r requirements.txt`. 
#### Ensure that python3 is already installed on your machine
#### 3. Using a cav file with the column name `U.S. DOT#:`, run the following command `python .\src\USDotScraperDriver.py -f filename.csv`
#### If you are in the src folder, ommit the src part in the command


