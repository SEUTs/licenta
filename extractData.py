import json
from csv import writer
import time
import requests
import os

def getChampionNames(frames): 
    #I HATE PICKING THE NAMES SO MUCH
    championNames = [[] for _ in range(11)]

    for frame in frames:
        events = frame.get("events")
        for event in events:
            type = event.get("type")
            if type == "CHAMPION_KILL":
                victimId = event.get("victimId")

                victimDamageDealt = event.get("victimDamageDealt")
                if victimDamageDealt is not None:
                    victimName = victimDamageDealt[0].get("name")
                    championNames[victimId].append(victimName)

                victimDamageReceived = event.get("victimDamageReceived")
                if victimDamageReceived is not None:
                    for damage in victimDamageReceived:
                        type = damage.get("type")
                        if type != "MINION" and type != "TOWER" and type != "MONSTER":
                            takedownerId = damage.get("participantId")
                            takedownerName = damage.get("name")
                            championNames[takedownerId].append(takedownerName)
    
    championNames = championNames[1:]
    # Thank you, RIOT GAMES, for having me create a nameProbabilityVector. Appreciated!

    correctedChampionNames = {
        "MonkeyKing": "Wukong",
        "JarvanIV": "Jarvan_IV",
        "Khazix": "Kha'Zix",
        "Kaisa": "Kai'Sa",
        "RekSai": "Rek'Sai",
        "KogMaw": "Kog'Maw",
        "Chogath": "Cho'Gath",
        "Belveth": "Bel'Veth",
        "Velkoz": "Vel'Koz",
        "MissFortune": "Miss_Fortune",
        "TwistedFate": "Twisted_Fate",
        "Leblanc": "LeBlanc",
        "LeeSin": "Lee_Sin",
        "TahmKench": "Tahm_Kench",
        "XinZhao": "Xin_Zhao",
        "MasterYi": "Master_Yi",
        "DrMundo": "Dr._Mundo",
        "KSante": "K'Sante",
        "AurelionSol": "Aurelion_Sol",
        "Nunu&Willump": "Nunu_&_Willump",
        "Renata": "Renata_Glasc",
        "FiddleSticks": "Fiddlesticks"
    }
    for i in range(10):
        if not championNames[i]:
            championNames[i] = "Cappa"
        else:
            championNames[i] = max(set(championNames[i]), key=championNames[i].count)
            championNames[i] = correctedChampionNames.get(championNames[i], championNames[i])
        
    return championNames

def getChampionNamesAndKda(frames): 
    #I HATE PICKING THE NAMES SO MUCH
    championNames = [[] for _ in range(11)]
    championKills = [0 for _ in range(11)]
    championDeaths = [0 for _ in range(11)]
    championAssists = [0 for _ in range(11)]

    for frame in frames:
        events = frame.get("events")
        for event in events:
            type = event.get("type")
            if type == "CHAMPION_KILL":
                victimId = event.get("victimId")
                killerId = event.get("killerId")
                assisterIds = event.get("assistingParticipantIds")

                championDeaths[victimId] += 1
                championKills[killerId] += 1
                if assisterIds is not None:
                    for assisterId in assisterIds:
                        championAssists[assisterId] += 1

                victimDamageDealt = event.get("victimDamageDealt")
                if victimDamageDealt is not None:
                    victimName = victimDamageDealt[0].get("name")
                    championNames[victimId].append(victimName)

                victimDamageReceived = event.get("victimDamageReceived")
                if victimDamageReceived is not None:
                    for damage in victimDamageReceived:
                        type = damage.get("type")
                        if type != "MINION" and type != "TOWER" and type != "MONSTER":
                            takedownerId = damage.get("participantId")
                            takedownerName = damage.get("name")
                            championNames[takedownerId].append(takedownerName)
    
    championNames = championNames[1:]
    # Thank you, RIOT GAMES, for having me create a nameProbabilityVector. Appreciated!

    correctedChampionNames = {
        "MonkeyKing": "Wukong",
        "JarvanIV": "Jarvan_IV",
        "Khazix": "Kha'Zix",
        "Kaisa": "Kai'Sa",
        "RekSai": "Rek'Sai",
        "KogMaw": "Kog'Maw",
        "Chogath": "Cho'Gath",
        "Belveth": "Bel'Veth",
        "Velkoz": "Vel'Koz",
        "MissFortune": "Miss_Fortune",
        "TwistedFate": "Twisted_Fate",
        "Leblanc": "LeBlanc",
        "LeeSin": "Lee_Sin",
        "TahmKench": "Tahm_Kench",
        "XinZhao": "Xin_Zhao",
        "MasterYi": "Master_Yi",
        "DrMundo": "Dr._Mundo",
        "KSante": "K'Sante",
        "AurelionSol": "Aurelion_Sol",
        "Nunu&Willump": "Nunu_&_Willump",
        "Renata": "Renata_Glasc"
    }
    for i in range(10):
        if not championNames[i]:
            championNames[i] = "Cappa"
        else:
            championNames[i] = max(set(championNames[i]), key=championNames[i].count)
            championNames[i] = correctedChampionNames.get(championNames[i], championNames[i])
    # print(championNames)
        
    championKdas = (championKills[1:], championDeaths[1:], championAssists[1:])
    return (championNames, championKdas)

def writeSkillLevelUps(matchFile):
    if not os.path.isfile(matchFile):
        return
    with open(matchFile, 'r') as f:
        data = json.load(f)
        with open("skillLevelUps.txt", 'w') as g:
            result = [[] for _ in range(10)]
            frames = data["info"]["frames"]
            for frame in frames:
                events = frame["events"]
                for event in events:
                    if event["type"] == "SKILL_LEVEL_UP":
                        result[event["participantId"] - 1].append(event["skillSlot"])
            championNames = getChampionNamesAndKda(frames)[0]
            for index in range(10):
                g.write(championNames[index] + ": " + str(result[index]) + '\n')
            g.close()
        f.close()

def getSkillLevelUps(matchFile):
    if not os.path.isfile(matchFile):
        return [[] for _ in range(10)]
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()
        result = [[] for _ in range(10)]
        frames = data["info"]["frames"]
        for frame in frames:
            events = frame["events"]
            for event in events:
                if event["type"] == "SKILL_LEVEL_UP":
                    result[event["participantId"] - 1].append(event["skillSlot"])
        return result

def getTimeOfMatch(match):
    daysOfTheWeek = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]
    monthsOfTheYear = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    
    rts = match.get("info").get("frames")[0].get("events")[0].get("realTimestamp")
    result = {
        "dayOfWeek": (rts // 24 // 60 // 60 // 1000 - 4) % 7 + 1,
        "hour":       rts // 60 // 60 // 1000 % 24
    }
    return result

def getWinningTeam(match):
    return int(match.get("info").get("frames")[-1].get("events")[-1].get("winningTeam") / 100)
def getWinningTeamFromFile(matchFile):
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()
        return data.get("info").get("frames")[-1].get("events")[-1].get("winningTeam") / 100

def getPuuids(match):
    participants =  match.get("info").get("participants")
    result = {}
    for i in range(10):
        result.update({participants[i].get("puuid"): i+1})
    return result

def getplayerIndexInMatch(puuid, match):
    return getPuuids(match)[puuid]
def getChampionInMatch(index, champions):
    return champions[index]


def didIndexWin(index, match):
    winningTeam = getWinningTeam(match)
    # print(winningTeam)
    return index < 5 and winningTeam == 1 or \
           index > 4 and winningTeam == 2
def didPuuidWin(puuid, match):
    index = getPuuids(match)[puuid] - 1
    return didIndexWin(index, match)

 
api_key = ""
jsonFileName = "output/matchHistorySas.json"
csvFileName = "output/league_data.csv"
puuid = "j-TN5AM2Sx7KmVpJS0rmGH5Mmg94SpNuZNKWktS2tISOsjWe5ZM8xIkeZTJHwapP_0bAqvZQFyiEfQ"
hundredsOfMatches = 3
newFile = False
sleepingTime = 2
matchesPerApiCall = 20


def getMatchHistoryUrl(puuid: str, start: int = 0, count: int = 20): 
    return f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start={start}&count={count}&api_key={api_key}'
def getMatchTimelineUrl(matchId: int):
    return f'https://europe.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline?api_key={api_key}'

def extractUsefulMatchData(match):
    frames = match.get("info").get("frames")
    championNamesAndKda = getChampionNamesAndKda(frames)
    matchTimestamp = getTimeOfMatch(match)
    result = []
    for index in range(10):
        if championNamesAndKda[0][index] != "":
            result.append([
                championNamesAndKda[0][index], 
                didIndexWin(index, match), 
                matchTimestamp.get("hour"), 
                matchTimestamp.get("dayOfWeek")
            ])
    print(result)
    return result

def extractUsefulPlayerMatchData(match, playerPuuid):
    frames = match.get("info").get("frames")
    championNamesAndKda = getChampionNamesAndKda(frames)

    index = getplayerIndexInMatch(playerPuuid, match) - 1
    champions = championNamesAndKda[0]
    time = getTimeOfMatch(match)


    result = {
        "champion": getChampionInMatch(index, champions),
        "win": didPuuidWin(playerPuuid, match),
        "hour": time.get("hour"),
        "dayOfWeek": time.get("dayOfWeek")
    }
    return result

def tryToGetMatchIds(puuid, start, count):
    def getMatchIds(puuid: str, start: int = 0, count: int = 20):
        api_url = getMatchHistoryUrl(puuid, start, count)
        result =  requests.get(api_url).json()
        return result
    
    matchIds = getMatchIds(puuid, start, count)
    retries = 0
    while not isinstance(matchIds, list):
        retries += 1
        print(f"[STATUS]: [IDS]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
        time.sleep(sleepingTime)
        matchIds = getMatchIds(puuid, start, count)
    return matchIds
def tryToGetTimeline(matchId): 
    def getMatchTimeline(matchId: str):
        api_url = getMatchTimelineUrl(matchId)
        return requests.get(api_url).json()
    
    timeline = getMatchTimeline(matchId)
    retries = 0
    while timeline.get("status") is not None:
        retries += 1
        print(f"[STATUS]: [TIMELINE]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
        time.sleep(sleepingTime)
        timeline = getMatchTimeline(matchId)
    return timeline

def insertMatchesIntoJson(matchIds, jsonFile):
    print(matchIds)
    print("\n"
    "---------------------------\n"
    " WRITING MATCHES INTO JSON\n"
    "---------------------------\n"
    )
    outputFile = open (f'{jsonFile}', 'w')
    outputFile.write('[')

    for matchIdIndex in range(len(matchIds)):
        print(f"Getting timeline {matchIdIndex + 1}/{len(matchIds)}")
        timeline = tryToGetTimeline(matchIds[matchIdIndex])
        print(f"Timeline {matchIdIndex + 1}/{len(matchIds)} obtained")
            
        json.dump(timeline, outputFile)
        if matchIdIndex < len(matchIds) - 1:
            outputFile.write(',')
    outputFile.write(']')
    outputFile.close()
    print("\n"
    "------------------\n"
    " WRITING COMPLETE\n"
    "------------------\n"
    )
def extractDataFromJsonToCSV(i, writerObject):
    print(i)
    print("\n"
    "--------------------------\n"
    " WRITING MATCHES INTO CSV\n"
    "--------------------------\n"
    )
    data = json.load(i)
    for matchIndex in range(len(data)):
        usefulData = extractUsefulMatchData(data[matchIndex])

        # extracting for every player
        if True is True:
            for entry in usefulData:
                writerObject.writerow(entry)
            print(f"Data extracter for all champions from match {matchIndex + 1}/{len(data)}")
        else:
            if usefulData.get("champion") != "":
                writerObject.writerow(usefulData.values())
                print(f"Data extracted from match {matchIndex + 1}/{len(data)}")
            else:
                reason = " (INSUFFICIENT DATA)"
                if data[matchIndex].get("info").get("frames")[-1].get("timestamp") < 240000:
                    reason = " (REMAKE)"
                print(f"Data ignored for match {matchIndex + 1}/{len(data)}{reason}")
    print("\n"
    "------------------\n"
    " WRITING COMPLETE\n"
    "------------------\n"
    )

def matches_to_API_to_JSON_to_CSV(matchIds: list, jsonFileName: str, csvFileName:str):
    with open(jsonFileName, 'r') as jsonFile, open(csvFileName, 'a') as csvFile:
        writerObject = writer(csvFile)
        print("Writer created")
        # if newFile:
        #     writerObject.writerow(["champion", "win", "hour", "dayOfWeek"])
        #     print("First row written")

        matchCounter = 0
        for matchId in matchIds:
            matchCounter += 1
            # resetting the reader pointer or else England explodes
            jsonFile.seek(0)

            # getting the data is done automatically in insertMatchesIntoJson
            print(f"[SYSTEM]: Getting match {matchCounter} / {len(matchIds)}")
            insertMatchesIntoJson((matchId,), jsonFileName)
            extractDataFromJsonToCSV(jsonFile, writerObject)
        csvFile.close()


def puuid_to_API_to_JSON_to_CSV(jsonFileName: str, csvFileName: str, puuid: str):
    with open(jsonFileName, 'r') as jsonFile, open(csvFileName, 'a') as csvFile:
        writerObject = writer(csvFile)
        print("Writer created")
        if newFile:
            writerObject.writerow(["champion", "win", "hour", "dayOfWeek"])
            print("First row written")

        offset = 0
        for index in range(offset, hundredsOfMatches + offset):
            # resetting the reader pointer or else England explodes
            jsonFile.seek(0)

            # getting the data is done automatically in insertMatchesIntoJson
            print(f"[SYSTEM]: Getting matches {index * matchesPerApiCall} to {(index + 1) * matchesPerApiCall}")
            
            print("Getting match ids")
            matchIds = tryToGetMatchIds(puuid, index * matchesPerApiCall, matchesPerApiCall)
            if len(matchIds) == 0:
                print("[SYSTEM]: REACHED END OF ACCESSIBLE MATCH HISTORY")
                break
            print("Match ids obtained")
            
            insertMatchesIntoJson(matchIds, jsonFileName)
            extractDataFromJsonToCSV(jsonFile, writerObject)
        csvFile.close()

if __name__ == "__main__":
    puuid_to_API_to_JSON_to_CSV(jsonFileName, csvFileName, puuid)