from bs4 import BeautifulSoup
import os
import csv

d = {'title': [], 'price': [], 'discount': []}

for file in os.listdir("data"):
    with open(f"data/{file}", encoding='utf-8') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    title = soup.find("span", id="productTitle")
    title = title.get_text(strip=True) if title else "No Title"

    price = soup.find("span", class_="a-price-whole")
    price = price.get_text() if price else "No Price"

   

    discount = soup.find("span", class_="savingsPercentage")
    discount = discount.get_text(strip=True) if discount else "No discount"


    d['title'].append(title)
    d['price'].append(price)
    d['discount'].append(discount)

csv_filename = 'product_data_NewFile.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=d.keys())
    writer.writeheader()
    writer.writerows([dict(zip(d, row)) for row in zip(*d.values())])

print(f"Data saved to {csv_filename}")
