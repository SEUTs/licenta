import json
from os import listdir

def getMatchesWith(championList):
    listOfIds = []
    files = listdir("D:\\licenta\\reducedGames")
    curr = 0
    for file in files:
        curr += 1
        print(file)
        print(str(curr) + '/' + str(len(files)))
        with open("D:\\licenta\\reducedGames\\" + file, 'r') as f: 
            data = json.load(f)
            f.close()
        
        stop = False
        for champ in championList:
            found = False
            for winners in data["winners"]:
                if winners["name"] == champ:
                    found = True
                    break
            for losers in data["losers"]:
                if losers["name"] == champ:
                    found = True
                    break
                
            if found == False:
                stop = True
                
        if stop:
            continue
        
        listOfIds.append(file)
    return listOfIds

print(len(getMatchesWith(["Vayne", "Briar"])))