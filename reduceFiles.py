import json
import os
import extractData

def storeChampionsAndKills():
    existingFiles = os.listdir("D:\\licenta\\reducedGames")
    files = os.listdir("D:\\licenta\\games")
    current = 0
    total = len(files)
    for file in files:
        current += 1
        print(f"{current} / {total}")
        if file in existingFiles:
            continue
        
        won = []
        lost = []
        with open("D:\\licenta\\games\\" + file, 'r') as f:
            data = json.load(f)
            f.close()

            if "info" not in data:
                continue 
            
            if data["info"]["frames"][-1]["timestamp"] < 240000:
                continue
            
            winningTeam = extractData.getWinningTeam(data)
            if winningTeam not in [1, 2]:
                continue

            namesAndKdas = extractData.getChampionNamesAndKda(data["info"]["frames"])
            for i in range((winningTeam-1) * 5, winningTeam * 5):
                won.append({"name": namesAndKdas[0][i], "kda": [namesAndKdas[1][0][i], namesAndKdas[1][1][i], namesAndKdas[1][2][i]]})
            for i in range(10 - winningTeam * 5, 10 - (winningTeam-1) * 5):
                lost.append({"name": namesAndKdas[0][i], "kda": [namesAndKdas[1][0][i], namesAndKdas[1][1][i], namesAndKdas[1][2][i]]})
            
            output = {
                "timestamp": data["info"]["frames"][0]["events"][0]["realTimestamp"],
                "winners": won,
                "losers": lost
            }

            json_object = json.dumps(output, indent=4)
            
            with open("D:\\licenta\\reducedGames\\" + file, 'x') as g:
                g.write(json_object)
        
storeChampionsAndKills()