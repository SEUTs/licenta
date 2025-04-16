import json
from csv import writer
import time
import requests

def getChampionNamesAndKda(frames): 
    championNames = ["" for _ in range(11)]
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
                    championNames[victimId] = victimName

                victimDamageReceived = event.get("victimDamageReceived")
                if victimDamageReceived is not None:
                    for damage in victimDamageReceived:
                        type = damage.get("type")
                        if type != "MINION" and type != "TOWER" and type != "MONSTER":
                            takedownerId = damage.get("participantId")
                            takedownerName = damage.get("name")
                            championNames[takedownerId] = takedownerName
    
    championNames = championNames[1:]
    championKdas = (championKills[1:], championDeaths[1:], championAssists[1:])
    return (championNames, championKdas)

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
    return match.get("info").get("frames")[-1].get("events")[-1].get("winningTeam")
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


def didPuuidWin(puuid, match):
    index = getPuuids(match)[puuid]
    winningTeam = getWinningTeam(match)
    return index < 6 and winningTeam == 100 or \
           index > 5 and winningTeam == 200


 
api_key = "RGAPI-f10a772f-6eb3-4447-b771-9eae485c9092"
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

def extractUsefulMatchData(match, playerPuuid):
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

def insertMatchesIntoJson(puuid, start, count):
    print("Getting match ids")
    matchIds = tryToGetMatchIds(puuid, start, count)
    print("Match ids obtained")
    if len(matchIds) == 0:
        print("[SYSTEM]: REACHED END OF ACCESSIBLE MATCH HISTORY")
        return False

    print("\n"
    "---------------------------\n"
    " WRITING MATCHES INTO JSON\n"
    "---------------------------\n"
    )
    outputFile = open (f'{inputFile}', 'w')
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
    return True
def extractDataFromJsonToCSV(i, writerObject, puuid):
    print(i)
    print("\n"
    "--------------------------\n"
    " WRITING MATCHES INTO CSV\n"
    "--------------------------\n"
    )
    data = json.load(i)
    for matchIndex in range(len(data)):
        usefulData = extractUsefulMatchData(data[matchIndex], puuid)

        if usefulData.get("champion") is not "":
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
        if insertMatchesIntoJson(puuid, index * matchesPerApiCall, matchesPerApiCall) == False:
            break
        extractDataFromJsonToCSV(jsonFile, writerObject, puuid)
    csvFile.close()