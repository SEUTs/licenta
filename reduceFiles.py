import json
import os
import extractData

def storeChampionsAndKills():
    existingFiles = os.listdir("E:\\licenta\\reducedGames")
    files = os.listdir("E:\\licenta\\games")
    current = 0
    total = len(files)
    for file in files:
        current += 1
        print(f"{current} / {total}")
        if file in existingFiles:
            continue
        
        won = []
        lost = []
        with open("E:\\licenta\\games\\" + file, 'r') as f:
            data = json.load(f)
            f.close()

            if data["info"]["frames"][-1]["timestamp"] < 240000:
                continue
            
            winningTeam = extractData.getWinningTeam(data)
            if winningTeam not in [1, 2]:
                continue

            names = extractData.getChampionNames(data["info"]["frames"])
            
            for i in range((winningTeam-1) * 5, winningTeam * 5):
                won.append(names[i])
            for i in range(10 - winningTeam * 5, 10 - (winningTeam-1) * 5):
                lost.append(names[i])
            
            output = {
                "timestamp": data["info"]["frames"][0]["events"][0]["realTimestamp"],
                "winners": won,
                "losers": lost
            }

            json_object = json.dumps(output, indent=4)
            with open("E:\\licenta\\reducedGames\\" + file, 'x') as g:
                g.write(json_object)
        
storeChampionsAndKills()