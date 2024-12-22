import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

def scrape_items(category):
    os.makedirs("data", exist_ok=True)

    
    driver = webdriver.Edge()

    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    email = os.getenv('email')
    password = os.getenv('password')

    try:
        login_to_amazon(driver, email, password)
        for i in range(1, 3):
            driver.get(
                f"https://www.amazon.in/gp/bestsellers/books/ref={category}?ie=UTF8&pg={i}"
            )
            load_all_items(driver)

            elements = driver.find_elements(By.CLASS_NAME, "zg-grid-general-faceout")
            print(f"Number of elements found on page {i}: {len(elements)}")
            
            
            with ThreadPoolExecutor() as executor:
                
                executor.map(lambda elem, idx: process_element(elem, headers, idx, category), elements, range((i-1)*len(elements),(i-1)*len(elements) + len(elements)))

    finally:
        driver.quit()


def login_to_amazon(driver, email, password):
    """
    Automate the login process for Amazon using Selenium.
    """
    
    amazon_login_url = (
        "https://www.amazon.in/ap/signin"
        "?openid.return_to=https%3A%2F%2Fwww.amazon.in"
        "&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select"
        "&openid.assoc_handle=inflex"
        "&openid.mode=checkid_setup"
        "&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select"
        "&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
    )

    
    driver.get(amazon_login_url)
    time.sleep(2)  

    
    email_field = driver.find_element(By.ID, "ap_email")
    email_field.send_keys(email)
    driver.find_element(By.ID, "continue").click()

    time.sleep(2)  

    
    password_field = driver.find_element(By.ID, "ap_password")
    password_field.send_keys(password)
    driver.find_element(By.ID, "signInSubmit").click()

    time.sleep(5)  
    print("Logged in successfully!")


def load_all_items(driver):
    """
    Scroll down the page to load all lazy-loaded items.
    """
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def extract_product_url(html_content):
    """
    Extract the product URL from the element's HTML content.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    product_link = soup.find("a", {"class": "a-link-normal aok-block"})
    if product_link:
        return "https://www.amazon.in" + product_link["href"]
    return None


def process_element(elem, headers, file_number, category):
    """
    Process a single element asynchronously, fetch product details, and save the HTML.
    """
    html_content = elem.get_attribute("outerHTML")
    product_url = extract_product_url(html_content)

    if product_url:
        print(f"Extracted URL: {product_url}")
        
        fetch_and_save_product_page(product_url, headers, html_content, file_number)


def fetch_and_save_product_page(product_url, headers, html_content, file_number, category):
    """
    Fetch the product page HTML using requests and save the data.
    """
    product_html = fetch_product_page(url, headers)
    if product_html:
        
        with open(f"data/{category}_product_{file_number}.html", "w", encoding="utf-8") as f:
            f.write(product_html)


def fetch_product_page(url, headers):
    """
    Fetch the product page HTML using requests.
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}: Status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None


if __name__ == '__main__':
    categories = {'Books': 'zg_bs_pg_2_books', 
                  'Computers & Accessories': 'zg_bs_nav_computers_0', 
                  'Movies & TV Shows': 'zg_bs_nav_dvd_0',
                  'Music': 'zg_bs_nav_music_0',
                  'Grocery & Gourmet Foods': 'zg_bs_nav_grocery_0',
                  'Industrial & Scientific': 'zg_bs_nav_industrial_0',
                  'Home & Kitchen': 'zg_bs_nav_kitchen_0',
                  'Office Products': 'zg_bs_nav_office_0',
                  'Video Games': 'zg_bs_nav_videogames_0',
                  'Pet Supplies': 'Watches',
                  'Home Improvement': 'zg_bs_nav_home-improvement_0',
                  }
    for category, url in categories.items():
        print(f'Scraping category {category}')
        scrape_items(url)
