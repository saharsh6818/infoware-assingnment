# INFOWARE Web Scraper ASSIGNMENT 

Steps to execute the files:

1. first create the virtual environment
   
      python -m venv venv

3. Activate the virtual environment:
   
source venv/bin/activate (Linux)

.\venv\Scripts\activate (Windows)

5. Install requirements:
   
pip install -r requirements.txt

7. Add environment variables for login:
   
create a .env file

add

email='your_amazon_email'

password='your_amazon_password'

9. Execute the scraper and parser
    
python infoware.py

python collection.py 


File Structure:

infoware.py:

Scraper file, uses selenium to login to amazon and scrape the Best seller products for 10 categories and saves their html code for later parsing.
Scrolls down to load more products (Amazon uses lazy loading, we overcome this problem by scrolling)

collection.py:

parser that uses BeautifulSoup4 to extract the data from previously downloaded html files and creates a csv to save the data.
