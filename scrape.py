import requests
from bs4 import BeautifulSoup
import json

link = "https://wiki.leagueoflegends.com/en-us/Dark_Seal"
link = "https://wiki.leagueoflegends.com/en-us/List_of_items"
# Making a GET request

# check status code for response received
# success code - 200
# print(r)


# Parsing the HTML

def extractData(link):
    searchFor = "infobox-section-stacked"
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    found = soup.find(class_ = searchFor)
    if found is None:
        found = soup.find(class_ = "infobox")
        if found is not None:
            found = found.find(class_ = "tabbertab")
    result = []
    good = True
    if found:
        for row in found.find_all("div"):
            if good:
                result.append(row.text)
            good = not good
        return result
    else:
        print(link)
        return None
def processData(data):
    stats = {}
    for stat in data:
        value, name = stat.split(' ', 1)
        if value == '+':
            continue
        if value[-1] == '%':
            value = value[:-1]
        stats.update({name: int(value)})
    return stats

r = requests.get(link)
soup = BeautifulSoup(r.content, 'html.parser')
found = soup.find_all(class_ = "tlist")[0:7]
items = {}
for i in found:
    for child in i.find_all('a'):
        itemLink = "https://wiki.leagueoflegends.com" + child.attrs["href"]
        print(itemLink)
        extractedData = extractData(itemLink)
        processedData = processData(extractedData) if extractedData is not None else {}
        items.update({child.attrs["title"]: processedData})

with open("itemStats.json", "w") as f:
    f.write(json.dumps(items))
f.close()


# print(result)
# items = {}
# for tr in trs:
#     tds = tr.find_all('td')
#     items.update({tds[0].text: tds[2].text})

# print(items)
# json_object = json.dumps(items, indent=0)
# with open("items.json", 'w') as file:
#     file.write(json_object)