import json
import os
import extractData
import time
import licenta
import matplotlib as plt

wins = {}
met = {}

dir_path = r'E:\\licenta\\games'
def getWinrates():
    scanned = 0
    for file in os.listdir(dir_path):
        with open(dir_path + '\\' + file, 'r') as f:
            data = json.load(f)
            f.close()
            if data["info"]["frames"][-1]["timestamp"] < 240000:
                continue
            scanned += 1
            names = extractData.getChampionNames(data["info"]["frames"])
            winningTeam = extractData.getWinningTeam(data)
            rts = data.get("info").get("frames")[0].get("events")[0].get("realTimestamp")
            hour = rts // 60 // 60 // 1000 % 24 // 8
            for i in range((winningTeam-1) * 5, winningTeam * 5):
                updated = wins.get(names[i], {})
                updated.update({hour * 8: updated.get(hour * 8, 0) + 1})
                wins.update({names[i]: updated})
            for name in names:
                updated = met.get(name, {})
                updated.update({hour * 8: updated.get(hour * 8, 0) + 1})
                met.update({name: updated})
    result = {}

    for champion in met:
        entries = []
        for hour in range(0, 24, 8):
            entry = {"hour": hour, "wins": wins.get(champion, {}).get(hour, 0), "games": met.get(champion, {}).get(hour, 0)}
            entries.append(entry)
        result.update({champion: entries})

    # result.sort(key=lambda element: element[2]/element[3])
    
    # print(scanned)
    for champion in result:
        print(champion, result[champion])
        # print(f"{element[0]} ({element[1]}): {element[2]} / {element[3]}")
    
    json_object = json.dumps(result, indent=4)
    
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

getWinrates()