import requests
from bs4 import BeautifulSoup as bs
import json

champs = []
with open("samples/sample.json", 'r') as f:
    data = json.load(f)
    f.close()
    for champ in data:
        champs.append(champ)

wheelNames = ["Damage"]
for champion in champs:
    soup = bs(requests.get("https://wiki.leagueoflegends.com/en-us/" + champion).content, "html.parser")

    result = {}

    # DMG, toughness, control, mobility, utility
    values = []
    champboxes = soup.find(class_='infobox champion-upd')
    # for div in champboxes.find_all('div'):
    #     for a in div.find_all('a'):
    #         print("\n" + str(a.contents))
    print(soup.find(id_="champinfo-container"))
    wheel = soup.find(class_='infobox-section-cell').find("tbody")
    tds = wheel.find_all("td")
    for td in tds:
        values.append(td.contents[0])
    # print(values)
    
    break
print(champs[0])

"""
    "Aatrox": {
        "classes": [
            "Juggernaut"
        ],
        "range": "melee",
        "range": "ranged",
        "damage": {
            "type": "phyiscal",
            "type": "magic",
            "type": "mixed",
            "duration": "burst",
            "duration": "DPS",
            "target": "single",
            "target": "multiple",
            "value": 
        },
        "resistance": {
            "type": "burst",
            "type": "sustained",
            "value": 
        },
        "control": {
            "target": "single",
            "target": "multiple",
            "target": "mixed",
            "value": 
        },
        "mobility": {
            "type": "burst",
            "type": "sustained",
            "value": 
        },
        "utility": {
            "value": 
        }
    }
"""