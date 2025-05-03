import requests
from bs4 import BeautifulSoup
import json

link = "https://darkintaqt.com/blog/item-ids"
# Making a GET request
r = requests.get(link)

# check status code for response received
# success code - 200
# print(r)


# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
trs = soup.find_all('tr')[1:]
items = {}
for tr in trs:
    tds = tr.find_all('td')
    items.update({tds[0].text: tds[2].text})

# print(items)
# json_object = json.dumps(items, indent=0)
# with open("items.json", 'w') as file:
#     file.write(json_object)