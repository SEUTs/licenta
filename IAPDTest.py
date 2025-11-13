import os
import glob
import extractData
import json

path = "D:\\licenta\\games"
games = [path + "\\" + x for x in os.listdir(path)]
dates = {}
i = 0
for game in games:
    dates.update({game: os.path.getctime(game)})
    i += 1
    print(i)
sortedE = {k: v for k, v in sorted(dates.items(), key=lambda item: item[1])}

with open("sortedFileNames.json", 'w') as f:
    sor = json.dumps(list(sortedE.keys()), indent=4)
    f.write(sor)
    f.close()

# with open(games[0], 'r') as f:
#     data = json.load(f)
#     matchId = data["metadata"]["matchId"]
#     frames = data["info"]["frames"]
#     print(extractData.getChampionNames(frames))
#     print(games[0])