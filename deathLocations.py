import requests
import json
from matplotlib import pyplot as plt
import math

outputDirectory = "output"
# api_key = "RGAPI-7d5cc397-1c5f-41dc-ab01-39bf09e0e897"
api_key = "RGAPI-f10a772f-6eb3-4447-b771-9eae485c9092"
if 'status' in requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/50124?api_key={api_key}').json():
    raise Exception("INVALID API KEY")

def getPuuidUrl(gameName: str, tagLine: str):
    return f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}'
def getPuuid(gameName: str, tagLine: str):
    api_url = getPuuidUrl(gameName, tagLine)
    result = requests.get(api_url).json()
    print(result)
    return result.get("puuid")

myPuuid = '0eVFsOl4yyzV538TUwDUo9qLISJ4fKosKDlpi0f8M_NoXluWsVF1hk-YSt21YjgV2C3GPXfjV1lwfw'
myPuuid = getPuuid("pumnal", "0015")
print(myPuuid)


img = plt.imread("minimapDeaths.png")
plt.figure(figsize=(11, 5))

# input_file = open (f'{outputDirectory}/matchHistory.json', 'r')
# json_array = json.load(input_file)
# input_file.close()
input_file2 = open (f'{outputDirectory}/matchHistoryfergus123.json', 'r')
json_array = json.load(input_file2)
input_file2.close()

# print(len(json_array), len(json_array2))

WestJungle = ((1680, 4050, 6500, 1900), (5700, 5000, 7367, 11550))
NorthJungle = ((7300, 10000, 9250, 3200), (8140, 10750, 13400, 13100))
SouthJungle = ((4900, 7443, 11650, 5700), (4300, 6800, 2300, 1700))
EastJungle = ((12550, 13100, 10750, 8257), (3150, 9400, 10050, 7600))

NWRiver = ((1900, 6500, 7300, 3200), (11550, 7367, 8140, 13100))
SERiver = ((7443, 11650, 12550, 8257), (6800, 2300, 3150, 7600))

BlueTopLane = ((1680, 0, 0, 2550), (5700, 5700, 15000, 12325))
BlueMidLane = ((7850, 6900, 4050, 4900), (7200, 7754, 5000, 4300))
BlueBotLane = ((5700, 5700, 14800, 12100), (1700, 0, 0, 2725))

RedTopLane = ((9250, 9250, 0, 2550), (13400, 15000, 15000, 12325))
RedMidLane = ((7850, 6900, 10000, 10750), (7200, 7754, 10750, 10050))
RedBotLane = ((13100, 14800, 14800, 12100), (9400, 9400, 0, 2725))

regions = (WestJungle, SouthJungle, EastJungle, NorthJungle,
           NWRiver, SERiver, 
           BlueTopLane, BlueMidLane, BlueBotLane,
           RedTopLane, RedMidLane, RedBotLane)
regionNames = ("Blue Topside Jungle", "Blue Botside Jungle", "Red Botside Jungle", "Red Topside Jungle",
               "Topside River", "Botside River",
               "Blue Toplane", "Blue Midlane", "Blue Botlane",
               "Red Toplane", "Red Midlane", "Red Botlane",
               "Blue Base", "Red Base")

def updateDeathLocations(deathLocations, deathCoords):
    for index in range(len(deathCoords[0])):
        region = findRegion((deathCoords[0][index], deathCoords[1][index]))
        deathLocations[region] += 1
def findRegion(point):
    def isInsideQuadrilateral(point, corner1, corner2, corner3, corner4):
        def computeAreaTriangle(p1, p2, p3):
            return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2)

        area1 =  computeAreaTriangle(corner1, corner2, corner3)
        area1 += computeAreaTriangle(corner1, corner3, corner4)

        area2  = computeAreaTriangle(point, corner1, corner2)
        area2 += computeAreaTriangle(point, corner2, corner3)
        area2 += computeAreaTriangle(point, corner3, corner4)
        area2 += computeAreaTriangle(point, corner4, corner1)

        return area1 == area2

    for index in range(len(regions)):
        region = regions[index]
        if isInsideQuadrilateral((point[0], point[1]), 
                                 (region[0][0], region[1][0]), 
                                 (region[0][1], region[1][1]), 
                                 (region[0][2], region[1][2]), 
                                 (region[0][3], region[1][3])):
            return regionNames[index]
    if point[1] < 7500:
        return "Blue Base"
    else:
        return "Red Base"
deathLocations = {
    "Blue Base": 0,
    "Blue Toplane": 0,
    "Blue Midlane": 0,
    "Blue Botlane": 0,
    "Blue Topside Jungle": 0,
    "Blue Botside Jungle": 0,
    "Topside River": 0,
    "Botside River": 0,
    "Red Base": 0,
    "Red Toplane": 0,
    "Red Midlane": 0,
    "Red Botlane": 0,
    "Red Topside Jungle": 0,
    "Red Botside Jungle": 0
}
def drawGoldLines(times, minions, playerTeam, playerId): 
    plt.subplot(1, 2, 2)
    plt.title(f'CS in game {json_item_index + 1}')
    ax = plt.gca()
    ax.set_facecolor("#121212")
    plt.grid(color="#40404080")
    
    for player in range(10):
        # default enemy because 5/10 probability
        color = "#ff7070"
        facecolor = "#ff404040"
        
        # check if the player is an ally
        if player in range(playerTeam * 5, playerTeam * 5 + 5):
            color = "#7070ff"
            facecolor = "#4040ff40"
            # check if the player is the client
            if player == playerId:
                continue

        plt.plot(times, minions[player], c=color)
        plt.fill_between(times, 0, minions[player], facecolor=facecolor)

    plt.plot(times, minions[playerId], c="#ffff70")
    plt.fill_between(times, 0, minions[playerId], facecolor="#ffff4060") 
def getPlayerAlliesEnemiesDeaths(deaths, playerTeam, playerId):
    playerDeaths = [deaths[0][playerId], deaths[1][playerId]]
    playerDeaths = [[[] for _ in range(4)], [[] for _ in range(4)]]
    enemyDeaths = [[[] for _ in range(5)], [[] for _ in range(5)]]
def customScatters(pointsList, color):
    for points in pointsList:
        plt.scatter(points[0], points[1], c=color)
def getKDAstats(item):
    kills = [0 for _ in range(10)]
    deaths = [0 for _ in range(10)]
    assists = [0 for _ in range(10)]

    killCoords = [[[] for _ in range(10)], [[] for _ in range(10)]]
    deathCoords = [[[] for _ in range(10)], [[] for _ in range(10)]]
    assistCoords = [[[] for _ in range(10)], [[] for _ in range(10)]]

    frames = item.get("info").get("frames")
    
    for frame in frames:
        events = frame.get("events")
        for event in events:
            if event.get("type") == "CHAMPION_KILL":
                position = event.get("position")
                x = position.get('x')
                y = position.get('y')

                killer = event.get("killerId")
                killCoords[0][killer - 1].append(x)
                killCoords[1][killer - 1].append(y)
                kills[killer - 1] += 1

                victim = event.get("victimId")
                deathCoords[0][victim - 1].append(x)
                deathCoords[1][victim - 1].append(y)
                deaths[victim - 1] += 1

                killAsistants = event.get("assistingParticipantIds")
                if killAsistants is not None:
                    for killAsistant in killAsistants:
                        assistCoords[0][killAsistant - 1].append(x)
                        assistCoords[1][killAsistant - 1].append(y)
                        assists[killAsistant - 1] += 1
    result = {
        "kills": kills,
        "deaths": deaths,
        "assists": assists,
        "killCoords": killCoords,
        "deathCoords": deathCoords,
        "assistCoords": assistCoords
    }
    return result
def getPlayerIdAndTeam(item):
    playerTeam = 0
    playerId = 0
    participants = item.get("metadata").get("participants")
    for index in range(len(participants)):
        if participants[index] == myPuuid:
            playerId = index
            if playerId > 5:
                playerTeam = 1
            break
        
    return (playerId, playerTeam)
def drawDeathPointsPlot(deaths, playerTeam, playerId):  
    plt.subplot(1, 2, 1)
    plt.title(f'Deaths in game {json_item_index + 1} ({teamPositions[playerId % 5]} for {teamColor[playerTeam]} Team)')
    plt.imshow(img, extent=[0, 14800, 0, 15000], aspect='auto')
    plt.axis('off')

    for player in range(10):
        # default enemy because 5/10 probability
        color = "r"
        
        # check if the player is the client
        if player == playerId:
            color = "#ffff00"
        
        # check if the player is an ally
        elif player in range(playerTeam * 5, playerTeam * 5 + 5):
            color = "b"

        plt.scatter(deaths[0][player], deaths[1][player], c=color)
def drawCreepScorePlot(item):
    frames = item["info"]["frames"]
    cs = [[] for _ in range(10)]
    times = []

    for frame in frames:
        for player in range(1, 11):
            minionsKilledByPlayer = frame["participantFrames"][str(player)]["minionsKilled"] + frame["participantFrames"][str(player)]["jungleMinionsKilled"]
            timestamp = frame["timestamp"] // 60000
            cs[player - 1].append(minionsKilledByPlayer)
        times.append(timestamp)
    drawGoldLines(times, cs, playerTeam, playerId)
def drawKDAPlot(kdaStatsArray): 
    myRange = range(len(kdaStatsArray))
    kdaRatios = [0 for _ in myRange]
    kills = [0 for _ in myRange]
    deaths = [0 for _ in myRange]
    assists = [0 for _ in myRange]
    
    for matchIndex in myRange:
        kills[matchIndex] = kdaStatsArray[matchIndex].get("kills")[playerId]
        deaths[matchIndex] = kdaStatsArray[matchIndex].get("deaths")[playerId]
        assists[matchIndex] = kdaStatsArray[matchIndex].get("assists")[playerId]
        
        kdaRatios[matchIndex] = kills[matchIndex] + assists[matchIndex]
        if deaths[matchIndex] != 0:
            kdaRatios[matchIndex] /= deaths[matchIndex]

    myRange = range(1, len(kdaStatsArray) + 1)
    plt.title(f'KDA over games')
    plt.figure(figsize=(11, 5))

    plt.subplot(1, 2, 1)
    plt.gca().set_facecolor("#121212")
    plt.grid(color="#40404080")
    
    plt.xticks(myRange)
    plt.plot(myRange, assists, linewidth=2, c="#00ff00")
    plt.plot(myRange, kills, linewidth=2, c="#ffff00")
    plt.plot(myRange, deaths, linewidth=2, c="#ff0000")
    plt.legend(["kills", "deaths", "assists"])
    
    plt.subplot(1, 2, 2)
    plt.gca().set_facecolor("#121212")
    plt.grid(color="#40404080")
    
    plt.xticks(myRange)
    plt.yticks(range(0, math.ceil(max(kdaRatios)) + 1))
    plt.plot(myRange, kdaRatios, linewidth=2, c="#7070ff")
    plt.legend(["KDA"])

teamPositions = ["Top", "Jungle", "Mid", "Bot", "Support"]
teamColor = ["Blue", "Red"]
json_item_index = 0
kdaStatsArray = []
for item in json_array:
    # gettingDeathStats
    kdaStats = getKDAstats(item)
    kdaStatsArray.append(kdaStats)
    (playerId, playerTeam) = getPlayerIdAndTeam(item)
    if playerId == 0:
        print("[ERROR]: PLAYER NOT FOUND BY PUUID")
        break

    playerDeathsCoords = [kdaStats.get("deathCoords")[0][playerId], kdaStats.get("deathCoords")[1][playerId]]
    updateDeathLocations(deathLocations, playerDeathsCoords)

    # TODO: Add subplot coordinates
    drawDeathPointsPlot(kdaStats.get("deathCoords"), playerTeam, playerId)
    drawCreepScorePlot(item)
    plt.savefig("output/result" + str(json_item_index) + ".png")
    
    json_item_index += 1
    plt.clf()
    
drawKDAPlot(kdaStatsArray)
plt.savefig("output/kdaResult.png")

def dictWithMergedLanes(originalDict: dict):
    returnedDict = {}
    returnedDict["Blue Base"] = originalDict["Blue Base"]
    returnedDict["Red Base"] = originalDict["Red Base"]
    returnedDict["Toplane"] = originalDict["Blue Toplane"] + originalDict["Red Toplane"]
    returnedDict["Midlane"] = originalDict["Blue Midlane"] + originalDict["Red Midlane"]
    returnedDict["Botlane"] = originalDict["Blue Botlane"] + originalDict["Red Botlane"]
    returnedDict["Topside River"] = originalDict["Topside River"]
    returnedDict["Botside River"] = originalDict["Botside River"]
    returnedDict["Blue Topside Jungle"] = originalDict["Blue Topside Jungle"]
    returnedDict["Blue Botside Jungle"] = originalDict["Blue Botside Jungle"]
    returnedDict["Red Topside Jungle"] = originalDict["Red Topside Jungle"]
    returnedDict["Red Botside Jungle"] = originalDict["Red Botside Jungle"]

    return dict(sorted(returnedDict.items(), key=lambda item: -item[1]))

# print(deathLocations)
sum = 0
for i in deathLocations:
    sum += deathLocations[i]
    
displayableDeaths = dictWithMergedLanes(deathLocations)
def printDeaths(displayableDeaths):
    for i in displayableDeaths:
        print(f'{i}: {displayableDeaths[i]}/{sum} ({round(displayableDeaths[i] * 100 / sum, 2)}%)')
# print(f'Total deaths: {sum}')


def plotMapRegionPoints():
    plt.scatter(WestJungle[0], WestJungle[1], c='#ff8000')
    plt.scatter(NorthJungle[0], NorthJungle[1], c='#804000')
    plt.scatter(SouthJungle[0], SouthJungle[1], c='#804000')
    plt.scatter(EastJungle[0], EastJungle[1], c='#ff8000')

    plt.scatter(BlueTopLane[0], BlueTopLane[1], c='b')
    plt.scatter(BlueMidLane[0], BlueMidLane[1], c='b')
    plt.scatter(BlueBotLane[0], BlueBotLane[1], c='b')
    plt.scatter(RedTopLane[0], RedTopLane[1], c='r')
    plt.scatter(RedMidLane[0], RedMidLane[1], c='r')
    plt.scatter(RedBotLane[0], RedBotLane[1], c='r')



# print(f'Games analyzed: {len(json_array)}')