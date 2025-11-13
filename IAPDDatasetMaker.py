import os
import glob
import extractData, licenta
import json
import getMastery
import math
import myShapley

path = "D:\\licenta\\games"
games = [path + "\\" + x for x in os.listdir(path)]
    
# games.sort(key=os.path.getctime)

# with open("sortedFileNames.json", 'x') as f:
#     sor = json.dumps(games, indent=4)
#     f.write(sor)
#     f.close()

# with open(games[0], 'r') as f:
#     data = json.load(f)
#     matchId = data["metadata"]["matchId"]
#     frames = data["info"]["frames"]
#     print(extractData.getChampionNames(frames))
#     print(games[0])

characteristics = {}
with open("championCharacteristics.json", 'r') as f:
    characteristics = json.load(f)

def getTop3Classes(credentials: list, region: str):
    topClasses = [[characteristics[x[0]]["classes"], x[1]] for x in getMastery.getTopNChamps(credentials, region, -1)]
    result = {}
    for cs in topClasses:
        for c in cs[0]:
            result.update({c: result.get(c, 0) + cs[1]})
    return list(result)[:3]

# print(getTop3Classes(["SasEUnTicnit", "SEUTs"], "EUNE"))

def getCounterFactor(masteryPoints: int):
    a = 0.001
    return math.log(a*masteryPoints+1) / math.log(a * 1000000 + 1)

# print(myShapley.versusWinrate(["Garen", "Darius"]))
# print(myShapley.versusWinrate(["Darius", "Garen"]))

def getDataForDataset(lastMatchFile, matchFile, nextMatchFile, playerIndex):
    matchData = {}
    with open(matchFile, 'r') as f:
        matchData = json.load(f)
    
    result = {}
        
    puuid = matchData["info"]["participants"][playerIndex]["puuid"]
    playerClasses = getTop3Classes(puuid, "EUNE")
    result.update({"playerClass1": playerClasses[0], "playerClass2": playerClasses[1], "playerClass3": playerClasses[2]})
    
    
    enemyIndex = playerIndex - 5 if playerIndex > 4 else playerIndex + 5
    enemyPuuid = matchData["info"]["participants"][enemyIndex]["puuid"]
    enemyClasses = getTop3Classes(enemyPuuid, "EUNE")
    result.update({"enemyClass1": enemyClasses[0], "enemyClass2": enemyClasses[1], "enemyClass3": enemyClasses[2]})
    
    playerTop5Champions, playerMastery = getMastery.getTop5ChampsAndTotalMasteries(puuid, "EUNE")
    enemyTop5Champions, enemyMastery = getMastery.getTop5ChampsAndTotalMasteries(enemyPuuid, "EUNE")
    
    winrates = []
    for pc in playerTop5Champions:
        for ec in enemyTop5Champions:
            winrate = myShapley.versusWinrate([pc[0], ec[0]])
            if winrate is not None:
                winrates.append(winrate * (getCounterFactor(pc[1]) / getCounterFactor(ec[1])))
    winrates = sum(winrates) / len(winrates)
    result.update({"winrateFactor": winrates})
    
    result.update({"playedAtHour": matchData["info"]["frames"][0]["events"][0]["realTimestamp"] // 60 // 60 // 1000 % 24})
    
    result.update({"playerMastery": playerMastery})
    result.update({"enemyMastery": enemyMastery})
    
    result.update({"hoursBetweenMatches": getTimeDistanceBetweenMatches(lastMatchFile, matchFile)})
    
    lastMatchData = {}
    with open(lastMatchFile, 'r') as f:
        lastMatchData = json.load(f)
        
    result.update({"wonLastGame": extractData.didIndexWin(playerIndex, lastMatchData)})
    
    result.update({"hoursTillNextGame": getTimeDistanceBetweenMatches(matchFile, nextMatchFile)})
    
    return result
    
# dataForDataset = getDataForDataset(games[0], 0)
# print(dataForDataset)
# print(len(dataForDataset))

sortedByCDate = []
with open ("sortedFileNames.json", 'r') as f:
    sortedByCDate = json.load(f)

lastGamePlayers = set()
lastMatch = ""
thisGamePlayers = set()
thisMatch = ""
matchesLinkedByPlayer = []


def getTimeDistanceBetweenMatches(match1File, match2File):
    timestamp1 = 0
    timestamp2 = 0
    with open(match1File, 'r') as f:
        timestamp1 = json.load(f)["info"]["frames"][0]["events"][0]["realTimestamp"] // 60 // 60 // 1000
    with open(match2File, 'r') as f:
        timestamp2 = json.load(f)["info"]["frames"][0]["events"][0]["realTimestamp"] // 60 // 60 // 1000
    return abs(timestamp2 - timestamp1)

start = 2 # 0 is firstMatch, 1 is thisMatch. Can't compare them with -2 and -1

for nextMatchIndex in range(start, min(len(sortedByCDate), 1000)):
    # # matchData = {}
    # # with open (file, 'r') as f:
    # print(getDataForDataset(file, 0))
    nextMatchData = {}
    with open(sortedByCDate[nextMatchIndex], 'r') as f:
        nextMatchData = json.load(f)
    
    nextGamePlayers = set()
    for p in nextMatchData["info"]["participants"]:
        nextGamePlayers.add(p["puuid"])
        
    i = 0
    for p in nextGamePlayers:
        if p in lastGamePlayers and p in thisGamePlayers:
            matchesLinkedByPlayer.append((lastMatch, thisMatch, sortedByCDate[nextMatchIndex], p, i))
        i += 1
    
    lastGamePlayers = thisGamePlayers
    lastMatch = thisMatch
    thisGamePlayers = nextGamePlayers
    thisMatch = sortedByCDate[nextMatchIndex]
    
    print(f"Scanned {nextMatchIndex} / 3000. Found {len(matchesLinkedByPlayer)} matches! ")
    if (len(matchesLinkedByPlayer) == 168):
        matchesLinkedByPlayer = []
    
addToDataset = []

# DONEFOR = 0
# for m in matchesLinkedByPlayer:
# #     print(m)
#     addToDataset.append(getDataForDataset(lastMatchFile=m[0], matchFile=m[1], nextMatchFile=m[2], playerIndex=m[4]))
#     DONEFOR += 1
#     print("DONE FOR " + str(DONEFOR))
#     if DONEFOR == 168:
#         break
# # print(len(matchesLinkedByPlayer))

# JSONifiedDataset = json.dumps(addToDataset, indent=4)
# with open("IAPDDataset2.json", "w") as f:
#     f.write(JSONifiedDataset)
#     f.close()