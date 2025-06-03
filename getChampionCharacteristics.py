import requests
from bs4 import BeautifulSoup as bs
import json

champs = []
with open("samples/sample.json", 'r') as f:
    data = json.load(f)
    f.close()
    for champ in data:
        champs.append(champ)
champs.remove("Cappa")
usefulDivs = [
    [2, True, [
        [0, True, 
                [2, True, 
                    [0, False, 'span', [2]]
                ]
            ]
        ]
    ]
]

def getPlaystyle(functionSoup):
    return functionSoup.find_all('div')[7].find_all('span')[3]["title"]
def getDifficulty(functionSoup):
    return functionSoup.find_all('div')[9]["title"][-2]
def getClass(functionSoup):
    types = []
    spans = functionSoup.find_all('div')[20].find_all('span')
    for i in range(0, len(spans), 2):
        types.append(spans[i]['data-tip'])
    return types
def getRange(functionSoup):
    return functionSoup.find_all('div')[-4].find_all('a')[-1].contents
def getDamageType(functionSoup):
    return functionSoup.find_all('div')[-1].find_all('a')[-1].contents
def getWheelValues(functionSoup):
    wheel = functionSoup.find(class_='infobox-section-cell').find("tbody")
    tds = wheel.find_all("td")
    values = {}
    wheelNames = ["damage", "toughness", "control", "mobility", "utility"]
    for i in range(len(tds)):
        values.update({wheelNames[i]: tds[i].contents[0]})
    return values

# def getOtherData(functionSoup, reducedUsefulDivs, result):
#     for div in reducedUsefulDivs:
#         if div[1] == True:
#             print('\n\n', div[0], functionSoup, type(functionSoup))
#             returnedThings = getOtherData(functionSoup.find_all('div')[div[0]], div[2], result)
#             for thing in returnedThings:
#                 result.append(thing)
#         else:
#             return functionSoup.find('span')[div[0]]


def extractData(champs):
    result = {}
    increment = 0
    for champion in champs:
        soup = bs(requests.get("https://wiki.leagueoflegends.com/en-us/" + champion).content, "html.parser")
        championCharacteristics = {}

        # DMG, toughness, control, mobility, utility
        bigBox = soup.find(class_='infobox champion-upd')
        championCharacteristics.update({"difficulty": getDifficulty(bigBox)})
        championCharacteristics.update({"playstyle": getPlaystyle(bigBox)})
        championCharacteristics.update({"class": getClass(bigBox)})
        championCharacteristics.update({"range": getRange(bigBox)})
        championCharacteristics.update({"damageType": getDamageType(bigBox)})
        championCharacteristics.update({"values": getWheelValues(bigBox)})
        result.update({champion: championCharacteristics})
        # for div in bigBox.find_all('div'):
        #     print("\n\n", div.contents)


                # for a in div.find_all('a'):
                #     print("\n" + str(a.contents))
        # print(soup.find(id_="champinfo-container"))
        # print(values)
        
        print(champion)
        increment += 1
        print(f"{increment}/170")
    print(result)

def resetJson():    
    if False: # DON'T PRESS THIS
        with open("championCharacteristics.json", 'r') as f:
            data = json.load(f)
            f.close()
        
        for champ in champs:
            values = data[champ]["values"]
            values.update({
                "damage": {
                    "value": values["damage"]["value"],
                    "type": values["damage"]["type"],
                    "duration1": "burst",
                    "duration2": "DPS",
                    "target1": "single",
                    "target2": "multiple"
                },
                "toughness": {
                    "value": values["toughness"]["value"],
                    "type1": "burst",
                    "type2": "sustained"
                },
                "control": {
                    "value": values["control"]["value"],
                    "target1": "single",
                    "target2": "multiple",
                    "target3": "mixed"
                },
                "mobility": {
                    "value": values["mobility"]["value"],
                    "type1": "burst",
                    "type2": "sustained"
                },
                "utility": {
                    "value": values["utility"]["value"]
                }
            })
            data[champ].update({"values": values})

        
        json_object = json.dumps(data, indent=4)
        with open("championCharacteristics.json", 'w') as f:
            f.write(json_object)
            f.close()

def fintermediateJsonFormatting():
    with open("championCharacteristics.json", 'r') as f:
        data = json.load(f)
        f.close()
    champs = [champ for champ in data]
    for champ in champs:
        values = data[champ]["values"]
        if "duration1" in values["damage"]:
            values["damage"].update({"duration": values["damage"]["duration1"]})
            values["damage"].pop("duration1")
        else:
            values["damage"].update({"duration": values["damage"]["duration2"]})
            values["damage"].pop("duration2")
            
        if "target1" in values["damage"]:
            values["damage"].update({"target": values["damage"]["target1"]})
            values["damage"].pop("target1")
        else:
            values["damage"].update({"target": values["damage"]["target2"]})
            values["damage"].pop("target2")
            
        if "type1" in values["toughness"]:
            values["toughness"].update({"type": values["toughness"]["type1"]})
            values["toughness"].pop("type1")
        else:
            values["toughness"].update({"type": values["toughness"]["type2"]})
            values["toughness"].pop("type2")
            
        if "target1" in values["control"]:
            values["control"].update({"target": values["control"]["target1"]})
            values["control"].pop("target1")
        elif "target2" in values["control"]:
            values["control"].update({"target": values["control"]["target2"]})
            values["control"].pop("target2")
        else:
            values["control"].update({"target": values["control"]["target3"]})
            values["control"].pop("target3")
            
        if "type1" in values["mobility"]:
            values["mobility"].update({"type": values["mobility"]["type1"]})
            values["mobility"].pop("type1")
        else:
            values["mobility"].update({"type": values["mobility"]["type2"]})
            values["mobility"].pop("type2")
        data[champ].update({"values": values})

    json_object = json.dumps(data, indent=4)
    with open("championCharacteristics.json", 'w') as f:
        f.write(json_object)
        f.close()    

def finishJsonFormatting():
    with open("championCharacteristics.json", 'r') as f:
        data = json.load(f)
        f.close()
    champs = [champ for champ in data]
    for champ in champs:
        values = data[champ]["values"]

        values["damage"].update({"damageType": values["damage"]["type"]})
        values["damage"].pop("type")
        values["damage"].update({"damageTarget": values["damage"]["target"]})
        values["damage"].pop("target")
            
        values["toughness"].update({"toughnessType": values["toughness"]["type"]})
        values["toughness"].pop("type")

        values["control"].update({"controlTarget": values["control"]["target"]})
        values["control"].pop("target")
            
        values["mobility"].update({"mobilityType": values["mobility"]["type"]})
        values["mobility"].pop("type")

    json_object = json.dumps(data, indent=4)
    with open("championCharacteristics.json", 'w') as f:
        f.write(json_object)
        f.close()    
    
if __name__ == "__main__":
    finishJsonFormatting()
        

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