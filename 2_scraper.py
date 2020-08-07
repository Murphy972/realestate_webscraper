import requests
from bs4 import BeautifulSoup
import csv
import os
from csv import writer
from datetime import date

today = date.today()

open("craigslist_rental_listings_" + str(today) + ".csv", "x")
current_file = "craigslist_rental_listings_" + str(today) + ".csv"

response = requests.get('https://philadelphia.craigslist.org/search/apa?search_distance=1&postal=08028&availabilityMode=0&sale_date=all+dates')

soup = BeautifulSoup(response.text, 'html.parser')

posts = soup.find_all(class_="result-row")
num = 0
with open(current_file, mode='a', newline='') as f:
    fieldnames = ['Num', 'Id', 'Upload Date', 'Price', 'Bedrooms/sqr-ft', 'Location', 'Contact']
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()

for post in posts:
    num += 1
    price = post.find(class_="result-price").get_text()
    location = post.find(class_="nearby").get_text()
    bedrooms_unordered = post.find(class_="housing").get_text()
    bedrooms = str.join(" ", bedrooms_unordered.splitlines())
    upload_date = post.find(class_="result-date").get_text()
    array_id = [item["data-id"] for item in post.find_all() if "data-id" in item.attrs]
    contact = post.find(class_="mailapp")
    id = array_id[0]
    with open(current_file, mode='a', newline='') as f:
        fieldnames = ['Num', 'Id', 'Upload Date', 'Price', 'Bedrooms/sqr-ft', 'Location', 'Contact']
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writerow({'Id': id,
                             'Num': num,
                             'Upload Date': upload_date,
                             'Price': price,
                             'Location': location,
                             'Bedrooms/sqr-ft': bedrooms.replace(" ", ""),
                             'Contact': contact})

    print(id)
    print(num)
    print(upload_date)
    print(price)
    print(location)
    print(bedrooms)
    print("")



    # print(response.status_code)
