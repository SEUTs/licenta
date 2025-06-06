import json
import extractData
import licenta
import os
import time
import deathLocations

def saveMatchToFile(matchId):
    matchFile = "games\\Match_" + matchId + ".json"
    isFile = os.path.isfile(matchFile)
    if not (isFile):
        print(f"FILE {matchFile} ADDED!\n")
        data = licenta.getMatchTimeline(matchId)
        if data != {}:
            with open(matchFile, "x") as f:
                f.write(json.dumps(data))
            f.close()
    return matchFile

def getPlayerBuildPerMinute(playerId, matchFile):
    destroyedFor = []
    components = []
    def undoForComponents(event):
        result = []
        for component in components:
            if component[0] == event["beforeId"] and component[1] == event["participantId"]:
                for item in component[2]:
                   result.append(item)
        return result

    def getDestroyedComponents(event):
        result = []
        for index in range(len(destroyedFor)):
            entry = destroyedFor[index] # itemId, timestamp, participantId
            if event["timestamp"] == entry[1] and event["participantId"] == entry[2]:
                result.append(entry[0])
        return result

    items = {}
    with open("items.json", 'r') as f:
        items = json.load(f)
        f.close()

    jungleItems = [1101, 1102, 1103]
    healthPotAndControl = [2003, 2055]

    wards = [3330, 3340, 3348, 3363, 3364] #fiddle stealth arena farsight oracle
    runeItems = [2010, 2150, 2151, 2152, 2422] #cookies, rune elixirs and magical boots
    otherItems = [3865, 3866, 3867, 3513] #support items 1,2,3 and eye of herald
    elixirs = [2138, 2139, 2140] # elixirs
    matchId = ""
    result = []
    with open(matchFile, 'r') as f:
        timestampsOfPurchases = set()
        data = json.load(f)
        matchId = data["metadata"]["matchId"]
        frames = data["info"]["frames"]
        for frame in frames:
            events = frame["events"]
            for event in events:
                if event["type"][0:6] == "ITEM_P" and event["participantId"] == playerId:
                    timestampsOfPurchases.add(event["timestamp"])
        
        build = []
        for frame in frames:
            events = frame["events"]
            for event in events:
                if event["type"][0:4] == "ITEM" and event["participantId"] == playerId:
                    type = event["type"]
                    if type[5] == "P": #ITEM_PURCHASED
                        if event["itemId"] in wards:
                            for item in build:
                                if item in wards:
                                    build.remove(item)
                        if event["itemId"] in elixirs and len([x for x in build if x not in wards]) == 6:
                            continue
                        build.append(event["itemId"])
                        components.append([event["itemId"], event["participantId"], getDestroyedComponents(event)])
                        # print({event["itemId"]: getDestroyedComponents(event)})

                    elif type[5] == "D": #ITEM_DESTROYED
                        if event["itemId"] in jungleItems and event["itemId"] in build:
                            build.remove(event["itemId"])
                        if event["itemId"] in healthPotAndControl:
                            build.remove(event["itemId"])
                        elif event["itemId"] == 3003: #Archangel's Staff
                            build.remove(event["itemId"])
                            build.append(3040) #Seraph's Embrace
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 3119: #Winter's approach
                            build.remove(event["itemId"])
                            build.append(3121) #Fimbulwinter
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 3042: #Manamune
                            build.remove(event["itemId"])
                            build.append(3004) #Muramana
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 2420 and event["timestamp"] not in timestampsOfPurchases: #Seeker's Armguard
                            build.remove(event["itemId"])
                            build.append(2421) #Shattered Armguard
                        elif event["itemId"] not in wards and event["itemId"] not in runeItems and event["itemId"] not in otherItems and event["itemId"] not in elixirs:
                            if event["timestamp"] in timestampsOfPurchases:
                        # elif event["itemId"] in builds[event["participantId"] - 1]:
                                # print(event["itemId"], builds[event["participantId"] - 1], event["timestamp"])
                                build.remove(event["itemId"])
                                destroyedFor.append([event["itemId"], event["timestamp"], event['participantId']])

                    elif type[5] == "S": #ITEM_SOLD
                        pass
                        # print(event["timestamp"], items[str(event['itemId'])], event['itemId'], builds[event["participantId"] - 1])
                        build.remove(event["itemId"])

                    elif type[5] == "U": #ITEM_UNDO
                        if event["afterId"] in wards:
                            for item in build:
                                if item in wards:
                                    build.remove(item)
                        if event["beforeId"] != 0:
                            build.remove(event["beforeId"])
                            reAdd = undoForComponents(event)
                            # print(reAdd)
                            for item in reAdd:
                                build.append(item)
                        if event["afterId"] != 0:
                            build.append(event["afterId"])
            result.append(build.copy())
        f.close()
        
    for build in result:
    # print(result)
        found = False
        for ward in wards:
            if ward in build:
                build.remove(ward)
                build.insert(3, ward)
                found = True
        if not found:
            build.insert(3, wards[1])

    correctedItemIds = {
        3191: 2420,
        3192: 2421,
    }
    for build in result:
        for i in range(len(build)):
            build[i] = correctedItemIds.get(build[i], build[i])

    itemNames = [[items[str(x)] for x in build] for build in result]
    return (result, itemNames)

def getChampionsKDAsBuilds(matchFile = "singleMatch.json"):
    builds = [[] for _ in range(10)]
    
    destroyedFor = []
    components = []
    def undoForComponents(event):
        result = []
        for component in components:
            if component[0] == event["beforeId"] and component[1] == event["participantId"]:
                for item in component[2]:
                   result.append(item)
        return result

    def getDestroyedComponents(event):
        result = []
        for index in range(len(destroyedFor)):
            entry = destroyedFor[index] # itemId, timestamp, participantId
            if event["timestamp"] == entry[1] and event["participantId"] == entry[2]:
                result.append(entry[0])
        return result

    items = {}
    with open("items.json", 'r') as f:
        items = json.load(f)
        f.close()

    jungleItems = [1101, 1102, 1103]
    healthPotAndControl = [2003, 2055]

    wards = [3330, 3340, 3348, 3363, 3364] #fiddle stealth arena farsight oracle
    runeItems = [2010, 2150, 2151, 2152, 2422] #cookies, rune elixirs and magical boots
    otherItems = [3865, 3866, 3867, 3513, 3400, 3599, 3600] #support items 1,2,3, eye of herald, your cut and kalista's spears (2 of them for some reason)
    elixirs = [2138, 2139, 2140] # elixirs
    bootsEvolutionsToRoot = {
        3172: 3006, # Gunmetal Greaves => Berzerker's Greaves
        3174: 3047, # Armored Advance => Plated Steelcaps / Ninja Tabi
        3170: 3009, # Swiftmarch => Boots of Swiftness
        3175: 3020, # Spellslinger's Shoes => Sorcerer's Shoes
        3171: 3158, # Crimson Lucidity => Ionian Boots of Lucidity
        3013: 3010, # Synchronized Souls => Symbiotic Soles
        3173: 3111  # Chainlaced Crushers => Mercury's Treads
    }
    matchId = ""
    with open(matchFile, 'r') as f:
        timestampsOfPurchases = set()
        data = json.load(f)
        matchId = data["metadata"]["matchId"]
        frames = data["info"]["frames"]
        for frame in frames:
            events = frame["events"]
            for event in events:
                if event["type"][0:6] == "ITEM_P":
                    # print(event["type"], event["timestamp"])
                    timestampsOfPurchases.add(event["timestamp"])
        # print(timestampsOfPurchases)

        for frame in frames:
            events = frame["events"]
            for event in events:
                if event["type"][0:4] == "ITEM" and event["participantId"] != 0:
                    type = event["type"]
                    # if event["type"][0:4] == "ITEM" and event["type"][5] != "U":
                    #     print(event["timestamp"], event["type"], items[str(event["itemId"])], [items[str(x)] for x in builds[event["participantId"] - 1]])
                    # print(event["timestamp"], builds[6])
                    if type[5] == "P": #ITEM_PURCHASED
                        if event["itemId"] in wards:
                            for item in builds[event["participantId"] - 1]:
                                if item in wards:
                                    builds[event["participantId"] - 1].remove(item)
                        if event["itemId"] in elixirs and len([x for x in builds[event["participantId"] - 1] if x not in wards]) == 6:
                            continue
                        builds[event["participantId"] - 1].append(event["itemId"])
                        components.append([event["itemId"], event["participantId"], getDestroyedComponents(event)])
                        # print({event["itemId"]: getDestroyedComponents(event)})

                    elif type[5] == "D": #ITEM_DESTROYED
                        if event["itemId"] in jungleItems and event["itemId"] in builds[event["participantId"] - 1]:
                            builds[event["participantId"] - 1].remove(event["itemId"])
                        if event["itemId"] in healthPotAndControl and event["itemId"] in builds[event["participantId"] - 1]:
                            builds[event["participantId"] - 1].remove(event["itemId"])
                        elif event["itemId"] == 3003 and event["itemId"] in builds[event["participantId"] - 1]: #Archangel's Staff
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(3040) #Seraph's Embrace
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 3119 and event["itemId"] in builds[event["participantId"] - 1]: #Winter's approach
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(3121) #Fimbulwinter
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 3042 and event["itemId"] in builds[event["participantId"] - 1]: #Manamune
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(3004) #Muramana
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 2420 and event["timestamp"] not in timestampsOfPurchases and event["itemId"] in builds[event["participantId"] - 1]: #Seeker's Armguard
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(2421) #Shattered Armguard
                        elif event["itemId"] not in wards and event["itemId"] not in runeItems and event["itemId"] not in otherItems and event["itemId"] not in elixirs:
                            if event["timestamp"] in timestampsOfPurchases:
                        # elif event["itemId"] in builds[event["participantId"] - 1]:
                                # print(event["itemId"], builds[event["participantId"] - 1], event["timestamp"])
                                # print(event["itemId"])
                                if event["itemId"] in bootsEvolutionsToRoot and event["itemId"] not in builds[event["participantId"] - 1]:
                                    builds[event["participantId"] - 1].remove(bootsEvolutionsToRoot[event["itemId"]])
                                else:
                                    builds[event["participantId"] - 1].remove(event["itemId"])

                                destroyedFor.append([event["itemId"], event["timestamp"], event['participantId']])

                    elif type[5] == "S" and event["itemId"] not in runeItems and event["itemId"] not in otherItems: #ITEM_SOLD
                        pass
                        # print(event["timestamp"], items[str(event['itemId'])], event['itemId'], builds[event["participantId"] - 1])
                        builds[event["participantId"] - 1].remove(event["itemId"])

                    elif type[5] == "U": #ITEM_UNDO
                        if event["afterId"] in wards:
                            for item in builds[event["participantId"] - 1]:
                                if item in wards:
                                    builds[event["participantId"] - 1].remove(item)
                        if event["beforeId"] != 0:
                            builds[event["participantId"] - 1].remove(event["beforeId"])
                            reAdd = undoForComponents(event)
                            # print(reAdd)
                            for item in reAdd:
                                builds[event["participantId"] - 1].append(item)
                        if event["afterId"] != 0:
                            builds[event["participantId"] - 1].append(event["afterId"])
        f.close()
        
    result = list(extractData.getChampionNamesAndKda(frames))
    # print(result)
    result.append(builds)
    for build in builds:
        found = False
        for ward in wards:
            if ward in build:
                build.remove(ward)
                build.insert(3, ward)
                found = True
        if not found:
            build.insert(3, wards[1])

    correctedItemIds = {
        3191: 2420,
        3192: 2421,
    }
    for build in builds:
        for i in range(len(build)):
            build[i] = correctedItemIds.get(build[i], build[i])

    result.append([[items[str(x)] for x in build] for build in builds])
    result.append(matchId)
    # print(result)
    return result
    # def itemIdToNames(builds: list):
    #     for build in builds:
    #         for i in range(len(build)):
    #             build[i] = items[str(build[i])]
    #     return builds
    # builds = itemIdToNames(builds)

    # for build in builds:
    #     print(build)

    # print(components)
def getConvenientTimeFormat(timeInSeconds):
    timeUnits = timeInSeconds
    if timeUnits < 60:
        return f"{timeUnits} seconds ago"
    timeUnits = timeUnits // 60
    if timeUnits < 60:
        return f"{timeUnits} minutes ago"
    timeUnits = timeUnits // 60
    if timeUnits < 60:
        return f"{timeUnits} hours ago"
    timeUnits = timeUnits // 24
    return f"{timeUnits} days ago"

def getMatchPreview(puuid, matchFile):
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()
        userParticipantId = licenta.getParticipantIdInMatch(puuid, data)
        processed = getChampionsKDAsBuilds(matchFile)

        champion = processed[0][userParticipantId]

        kda = (processed[1][0][userParticipantId], processed[1][1][userParticipantId], processed[1][2][userParticipantId])

        build = processed[2][userParticipantId]

        win = "Victory" if extractData.didPuuidWin(puuid, data) else "Defeat"
        currentTimestamp = time.time()
        timeFromMatch = int(currentTimestamp) - data["info"]["frames"][0]["events"][0]["realTimestamp"] // 1000
        timeFromMatch = getConvenientTimeFormat(timeFromMatch)
        matchDuration = data["info"]["frames"][-1]["events"][-1]["timestamp"] // 1000
        matchDuration = f"{matchDuration // 60} min {matchDuration % 60} sec"
        details = (win, timeFromMatch, matchDuration)

        matchId = processed[4]

        result = (champion, details, kda, build, matchId)
        # print(result)
        return result
    
def getTeamGoldDifference(matchFile, playerTeam):
    data = getGoldPerMinuteForAll(matchFile)
    teamGoldDifferences = []
    teamMultiplier = 1 if playerTeam == 0 else -1
    for minute in data[0]:
        difference = 0
        for i in range(1, 6):
            # print(data[1][str(i)][minute])
            difference += data[1][str(i)][minute] * teamMultiplier
        for i in range(6, 11):
            difference -= data[1][str(i)][minute] * teamMultiplier
        teamGoldDifferences.append(difference)
    return teamGoldDifferences

def getGoldPerMinuteData(playerIndex, matchFile):
    enemyIndex = str(playerIndex + 5 if playerIndex < 6 else playerIndex - 5)
    playerIndex = str(playerIndex)
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()
        frames = data["info"]["frames"]
        goldData = [[], []]
        for frame in frames[:-1]:
            participantFrames = frame["participantFrames"]
            goldData[0].append(participantFrames[playerIndex]["totalGold"])
            goldData[1].append(participantFrames[enemyIndex]["totalGold"])

        lastFrameDataPlayer = frames[-1]["participantFrames"][playerIndex]
        lastFrameDataEnemy = frames[-1]["participantFrames"][enemyIndex]
        goldDifferencePlayer = lastFrameDataPlayer["totalGold"] - goldData[0][-1]
        goldDifferenceEnemy = lastFrameDataEnemy["totalGold"] - goldData[1][-1]
        multiplier = 60000 / (frames[-1]["timestamp"] % 60000)
        goldData[0].append(int(goldData[0][-1] + goldDifferencePlayer * multiplier))
        goldData[1].append(int(goldData[1][-1] + goldDifferenceEnemy * multiplier))
    return (([range(len(goldData[0])), goldData[0]], [range(len(goldData[1])), goldData[1]]))


def getGoldPerMinuteForAll(matchFile="E:\\licenta\\games\\Match_EUN1_3682989051.json"):
    data = ""
    # print("\n\n\n\n" + str(matchFile) + "\n\n\n\n")
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()

    frames = data["info"]["frames"]
    goldData = [[] for _ in range(10)]
    for frame in frames[:-1]:
        participantFrames = frame["participantFrames"]
        for player in participantFrames:
            goldData[int(player)-1].append(participantFrames[player]["totalGold"])

    multiplier = 60000 / (frames[-1]["timestamp"] % 60000)
    for i in range(10):
        lastFrameDataPlayer = frames[-1]["participantFrames"][str(i+1)]
        goldDifferencePlayer = lastFrameDataPlayer["totalGold"] - goldData[i][-1]
        goldData[i].append(int(goldData[i][-1] + goldDifferencePlayer * multiplier))

    result = {}    
    for i in range(10):
        result.update({str(i+1): goldData[i]})
    return ((range(len(goldData[0])), result))

def getDeathStats(matchFile="E:\\licenta\\games\\Match_EUN1_3682989051.json"):
    deaths = {}
    for i in range(1, 11):
        deaths.update({i: []})
    # dir_path = r'E:\\licenta\\games'
    # file = os.listdir(dir_path)[0]
    # with open(dir_path + '\\' + file, 'r') as f:
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()
        frames = data["info"]["frames"]
        for frame in frames:
            HPs = {}
            championStats = frame["participantFrames"]
            for i in range(1, 11):
                HPs.update({i: championStats[str(i)]["championStats"]["healthMax"]})
            events = frame["events"]
            for event in events:
                if event["type"] == "CHAMPION_KILL":
                    totalDamageReceived = [0, 0, 0, 0]
                    receivedFrom = {}
                    totalDamageDealt = 0
                    dealtTo = {}
                    for damageReceived in event["victimDamageReceived"]:
                        totalDamageReceived[0] += damageReceived["physicalDamage"]
                        totalDamageReceived[1] += damageReceived["physicalDamage"]
                        totalDamageReceived[0] += damageReceived["magicDamage"]
                        totalDamageReceived[2] += damageReceived["magicDamage"]
                        totalDamageReceived[0] += damageReceived["trueDamage"]
                        totalDamageReceived[3] += damageReceived["trueDamage"]
                        receivedFrom.update({damageReceived["participantId"]: receivedFrom.get(damageReceived["participantId"], 0) + damageReceived["physicalDamage"] + damageReceived["magicDamage"] + damageReceived["trueDamage"]})
                    for damageDealt in event.get("victimDamageDealt", []):
                        totalDamageDealt += damageDealt["physicalDamage"]
                        totalDamageDealt += damageDealt["magicDamage"]
                        totalDamageDealt += damageDealt["trueDamage"]
                        dealtTo.update({damageDealt["participantId"]: dealtTo.get(damageDealt["participantId"], 0) + damageDealt["physicalDamage"] + damageDealt["magicDamage"] + damageDealt["trueDamage"]})

                    # print(f"{totalDamageReceived[0]}/{HPs[event["victimId"]]}: {totalDamageReceived[1]}P {totalDamageReceived[2]}M {totalDamageReceived[3]}T\n{receivedFrom}")
                    # print(f"{totalDamageDealt}")
                    # for entry in dealtTo:
                    #     print(f"Dealt {dealtTo[entry]}/{HPs[entry]} to {entry}")

                    percentageReceived = round(totalDamageReceived[0]/HPs[event["victimId"]] * 100, 2)
                    percentageDealt = 0
                    if dealtTo:
                        percentageDealt = round(sum(dealtTo[x]/HPs[x] for x in dealtTo) * 100, 2)

                    # print(f"Percentage received: {percentageReceived}%")
                    # print(f"Percentage dealt: {percentageDealt}%")
                    # print("\n")

                    death = {
                        "victimHP": HPs[event["victimId"]],
                        "victimArmor": championStats[str(event["victimId"])]["championStats"]["armor"],
                        "victimMagicResist": championStats[str(event["victimId"])]["championStats"]["magicResist"],
                        "victimOmnivamp": championStats[str(event["victimId"])]["championStats"]["lifesteal"]
                                        + championStats[str(event["victimId"])]["championStats"]["omnivamp"]
                                        + championStats[str(event["victimId"])]["championStats"]["physicalVamp"],
                        "victimDamageReceived": {
                            "totalDamage": totalDamageReceived[0],
                            "physicalDamage": totalDamageReceived[1],
                            "magicDamage": totalDamageReceived[2],
                            "trueDamage": totalDamageReceived[3],
                        },
                        "totalDamageDealt": sum(dealtTo[x] for x in dealtTo),
                        "killersDamageReceived": [],
                        "timestamp": event["timestamp"],
                        "location": deathLocations.findRegion((event["position"]['x'], event["position"]['y']))
                    }
                    for entry in dealtTo:
                        death["killersDamageReceived"].append({
                            "killerId": entry,
                            "killerHP": HPs[entry],
                            "killerTotalDamage": dealtTo[entry]
                        })
                    updated = deaths[event["victimId"]]
                    updated.append(death)
                    deaths.update({event["victimId"]: updated})
    return deaths

def getDamageStatsOfAll(matchFile, playerRange):
    playerRange = [str(x) for x in playerRange]
    minuteStats = []
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()

        rawChampionStats = data["info"]["frames"][-1]["participantFrames"]
        
        frames = data["info"]["frames"]
        for frame in frames:
            rawChampionStats = frame["participantFrames"]
            stats = {}
            for champion in playerRange:
                rawDamageStats = rawChampionStats[champion]["damageStats"]
                rawValueStats = rawChampionStats[champion]["championStats"]
                processedStats = {
                    "physicalDamageDealt": rawDamageStats["physicalDamageDoneToChampions"],
                    "physicalDamageTaken": rawDamageStats["physicalDamageTaken"],
                    "magicDamageDealt": rawDamageStats["magicDamageDoneToChampions"],
                    "magicDamageTaken": rawDamageStats["magicDamageTaken"],
                    "trueDamageDealt": rawDamageStats["trueDamageDoneToChampions"],
                    "trueDamageTaken": rawDamageStats["trueDamageTaken"],
                    "omnivamp": rawValueStats["lifesteal"] + rawValueStats["omnivamp"] + rawValueStats["physicalVamp"]
                }
                stats.update({int(champion): processedStats})
            minuteStats.append(stats)
    # for stats in minuteStats:
    #     print(stats[int(playerRange[0])])
    return minuteStats