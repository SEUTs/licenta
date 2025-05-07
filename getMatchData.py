import json
import extractData
import licenta
import os
import time

def saveMatchToFile(matchId):
    matchFile = "Match_" + matchId + ".json"
    isFile = os.path.isfile(matchFile)
    if not (isFile):
        print(f"FILE {matchFile} ADDED!\n")
        data = licenta.getMatchTimeline(matchId)
        with open(matchFile, "x") as f:
            f.write(json.dumps(data))
        f.close()
    return matchFile

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
    otherItems = [3865, 3866, 3867, 3513] #support items 1,2,3 and eye of herald
    elixirs = [2138, 2139, 2140] # elixirs
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
                        if event["itemId"] in healthPotAndControl:
                            builds[event["participantId"] - 1].remove(event["itemId"])
                        elif event["itemId"] == 3003: #Archangel's Staff
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(3040) #Seraph's Embrace
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 3119: #Winter's approach
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(3121) #Fimbulwinter
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 3042: #Manamune
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(3004) #Muramana
                            timestampsOfPurchases.add(event["timestamp"])
                        elif event["itemId"] == 2420 and event["timestamp"] not in timestampsOfPurchases: #Seeker's Armguard
                            builds[event["participantId"] - 1].remove(event["itemId"])
                            builds[event["participantId"] - 1].append(2421) #Shattered Armguard
                        elif event["itemId"] not in wards and event["itemId"] not in runeItems and event["itemId"] not in otherItems and event["itemId"] not in elixirs:
                            if event["timestamp"] in timestampsOfPurchases:
                        # elif event["itemId"] in builds[event["participantId"] - 1]:
                                # print(event["itemId"], builds[event["participantId"] - 1], event["timestamp"])
                                builds[event["participantId"] - 1].remove(event["itemId"])
                                destroyedFor.append([event["itemId"], event["timestamp"], event['participantId']])

                    elif type[5] == "S": #ITEM_SOLD
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
        print(result)
        return result