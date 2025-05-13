import requests
import json
import time
import getMatchData
import base64
import io
import matplotlib.pyplot as plt
import numpy

gamesFolder = "E:\\licenta\\games"

# api_key = "RGAPI-6977ba4c-8a65-41f1-8766-d94feaf633d9"
# api_key = "RGAPI-231f39d7-da32-4266-a2fc-9c35f9d534be"
# api_key = "RGAPI-489a4027-3176-457e-ac43-fd5744ba5466"
# api_key = "RGAPI-7d5cc397-1c5f-41dc-ab01-39bf09e0e897"
api_key = "RGAPI-f10a772f-6eb3-4447-b771-9eae485c9092"
requests.get("https://www.google.com")
if 'status' in requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/50124?api_key={api_key}').json():
    raise Exception("INVALID API KEY")

outputDirectory = "output"

# print(getPuuid("pumnal", "0015"))

rankQueue = "RANKED_SOLO_5x5"
ranks = ("CHALLENGER", "GRANDMASTER", "MASTER", "DIAMOND", "EMERALD", "PLATINUM", "GOLD", "SILVER", "BRONZE", "IRON")
rankDistributions = (1, 1, 1, 4, 4, 4, 4, 4, 4, 4)
romans = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}


def getPuuid(gameName: str, tagLine: str):
    def getPuuidUrl(gameName: str, tagLine: str):
        return f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={api_key}'

    def aux(gameName: str, tagline: str):
        api_url = getPuuidUrl(gameName, tagLine)
        return requests.get(api_url).json().get("puuid")
    
    sleepingTime = 2
    matchIds = aux(gameName, tagLine)
    retries = 0

    while "status" in matchIds:
        retries += 1
        print(f"[STATUS]: [PUUID]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
        time.sleep(sleepingTime)
    matchIds = aux(gameName, tagLine)
    return matchIds   
def getMatchHistoryUrl(puuid: str, start: int = 0, count: int = 20): 
    return f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start={start}&count={count}&api_key={api_key}'
def getMatchStatsUrl(matchId: int):
    return f'https://europe.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={api_key}'
def getMatchTimelineUrl(matchId: int):
    return f'https://europe.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline?api_key={api_key}'
def GetMatchIds(puuid, start: int = 0, count: int = 20):
    def aux(puuid: str, start, count):
        api_url = getMatchHistoryUrl(puuid, start, count)
        return requests.get(api_url).json()
    
    sleepingTime = 2
    matchIds = aux(puuid, start, count)
    retries = 0

    while not isinstance(matchIds, list):
        retries += 1
        print(matchIds)
        print(f"[STATUS]: [IDS]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
        time.sleep(sleepingTime)
        matchIds = aux(puuid, start, count)
    return matchIds

def getChampionNames(link: str):
    def aux(link: str):
        api_url = getMatchStatsUrl(link)
        data = requests.get(api_url).json()
        return data
    
    sleepingTime = 2
    result = aux(link)
    retries = 0

    while "status" in result:
        retries += 1
        print(f"[STATUS]: [IDS]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
        time.sleep(sleepingTime)
        result = aux(link)
    return result
def getMatchTimeline(matchId: str):
    def aux(matchId: str):
        api_url = getMatchTimelineUrl(matchId)
        try:
            response = requests.get(api_url).json()
            if response.get("status_code") != 403:
                return response
            return {}
        except ValueError as ne:
            with open("E:\\licenta\\exceptions\\exceptions.txt", "a") as f:
                f.write(str(ne))
            return {}
    
    sleepingTime = 2
    result = aux(matchId)
    retries = 0

    while "status" in result:
        retries += 1
        print(f"[STATUS]: [IDS]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
        time.sleep(sleepingTime)
        result = aux(matchId)
    return result

    if 'status' in data:
        return # ! addWait

    info = data['info']
    statsParticipants = info['participants']
    participants = {}
    for participant in statsParticipants:
        participants.update({participant['participantId'] : participant['championName']})
    return participants
def getSlainForPastGames():
    count = 1
    results = 1
    for start in range(0, count * results, count):
        api_url = getMatchHistoryUrl(start, count)
        response = requests.get(api_url)

        if 'status' in response:
            break # ! addWait


        for link in response.json():
            participants = getChampionNames(link)
            api_url = getMatchTimelineUrl(link)
            data = requests.get(api_url).json()

            if 'status' in data:
                break # ! addWait

            info = data['info']
            frames = info['frames']
            for frame in frames:
                events = frame['events']
                for event in events:
                        if event['type'] == "CHAMPION_KILL":
                            killTime = event['timestamp']
                            killMinute = killTime // 60000 + 1
                            print(f"{participants[event['killerId']]} has slain {participants[event['victimId']]} at {killMinute}")
            
            # info = data['info']
            # frames = info['frames']
            # print(frames[0].keys())
            # for frame in frames:
            #     print(frame)
def getDeathsForLastGames(puuid: str, count = 20):
    api_url = getMatchHistoryUrl(count = count)
    response = requests.get(api_url).json()
    if 'status' in response:
        return # ! addWait
    
    overallDeaths = {}
    totalDeaths = 0

    countLinks = 0
    for link in response:
        api_url = getMatchTimelineUrl(link)
        data = requests.get(api_url).json()
        if 'status' in data:
            break # ! addWait

        countLinks += 1
        playerPUUIDs = data['metadata']['participants']
        participantId = playerPUUIDs.index(puuid) + 1

        participants = getChampionNames(link)
        participants.update({0: 0})
        #deaths = {}
        counter = 0
        for frame in data['info']['frames']:
            for event in frame['events']:
                if event['type'] == "CHAMPION_KILL":
                    if event['victimId'] == participantId:
                        counter += 1
                        killer = participants[event['killerId']]
                        overallDeaths.update({killer: (overallDeaths.get(killer) or 0) + 1})
        #                deaths.update({killer: (deaths.get(killer) or 0) + 1})
        #deaths.update({'total': counter})
        totalDeaths += counter
        #print(deaths)

        print(f'{countLinks * 100 // count}%')

    overallDeaths.update({'total': totalDeaths})
    overallDeaths = {k: v for k, v in sorted(overallDeaths.items(), key=lambda item: item[1])}
    print(overallDeaths)
def getSummonersWithRank(rank: str, rankDistribution: int, rankQueue = rankQueue, page: int = 1):
    def auxPage(rank, rankDistribution, rankQueue, page):
        api_url = f'https://eun1.api.riotgames.com/lol/league-exp/v4/entries/{rankQueue}/{rank}/{romans[rankDistribution]}?page={page}&api_key={api_key}'
        data = requests.get(api_url).json()
        return data
    def auxPuuid(entry):
        api_url = f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/{entry.get('summonerId')}?api_key={api_key}'
        data = requests.get(api_url).json()
        return data
    sleepingTime = 2

    SUMMONERS = auxPage(rank, rankDistribution, rankQueue, page)
    retries = 0
    while "status" in SUMMONERS:
        retries += 1
        print(SUMMONERS)
        print(f"[STATUS]: [GETTING SUMMONERS PAGE]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
        time.sleep(sleepingTime)
        SUMMONERS = auxPage(rank, rankDistribution, rankQueue, page)

    puuids = [summoner["puuid"] for summoner in SUMMONERS]
    # for summoner in SUMMONERS:
    #     data = auxPuuid(summoner)
    #     retries = 0
    #     while "status" in data:
    #         retries += 1
    #         print(f"[STATUS]: [GETTING PUUID]: Limit exceeded. Waiting {sleepingTime} seconds ({retries}/{120 // sleepingTime})")
    #         time.sleep(sleepingTime)
    #         data = auxPuuid(summoner)
    #     puuid = data.get("puuid")
    #     puuids.append(puuid)

    return puuids

    if count > len(data):
        count = len(data)

    puuids = []
    for entry in data:
        if len(puuids) >= count:
            break

        api_url = f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/{entry.get('summonerId')}?api_key={api_key}'
        data = requests.get(api_url).json()
        puuid = data.get("puuid")
        puuids.append(puuid)
    
    return puuids
def getKillsFromHistory():
    input_file = open (f'{outputDirectory}/matchHistory{username}.json', 'r')
    json_array = json.load(input_file)
    input_file.close()

    for item in json_array:
        killCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        frames = item.get("info").get("frames")
        for frame in frames:
            events = frame.get("events")
            for event in events:
                if event.get("type") == "CHAMPION_KILL":
                    killCount[event.get("killerId") - 1] += 1
        print(killCount)
def getDeathMap():
    input_file = open (f'{outputDirectory}/matchHistory.json', 'r')
    json_array = json.load(input_file)
    input_file.close()

    for item in json_array:
        killCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        frames = item.get("info").get("frames")
        for frame in frames:
            events = frame.get("events")
            for event in events:
                if event.get("type") == "CHAMPION_KILL":
                    killCount[event.get("killerId") - 1] += 1
        print(killCount)
def insertMatchesIntoFiles():
        outputFile = open (f'{outputDirectory}/matchHistory{username}.json', 'w')
        outputFile.write('[')

        myLast20MatchesIds = getMatchIds(myPuuid, 0, 100)
        for matchIdIndex in range(len(myLast20MatchesIds)):
            timeline = getMatchTimeline(myLast20MatchesIds[matchIdIndex])
            json.dump(timeline, outputFile)
            if matchIdIndex < len(myLast20MatchesIds) - 1:
                outputFile.write(',')

        outputFile.write(']')

def generateTeamGoldPlot(matchFile, playerTeam):
    teamGoldDifferences = getMatchData.getTeamGoldDifference(matchFile, playerTeam)
    xRange = range(len(teamGoldDifferences))
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#181864')
    ax.set_facecolor('#181864')
    ax.plot(xRange, teamGoldDifferences, c='w')
    ax.set_xlabel('Time (min)')
    ax.yaxis.labelpad = -5
    ax.set_ylabel('Total Gold')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    x = numpy.array(xRange)
    y = numpy.array(teamGoldDifferences)
    zeros = numpy.zeros_like(y)
    ax.fill_between(x, y, zeros, where=(y > zeros), color='#00FFFF', alpha=0.2, interpolate=True)
    ax.fill_between(x, y, zeros, where=(y <= zeros), color='r', alpha=0.4, interpolate=True)
    absMaxY = max([abs(y) for y in teamGoldDifferences]) * 1.1
    ax.set_ylim(-absMaxY, absMaxY)
    ax.tick_params(colors="white")
    ax.grid()
    ax.set_title("Team Gold Difference", color="white")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return image_base64

def generate2GoldPlot(player, matchFile):
    data = getMatchData.getGoldPerMinuteData(player, matchFile)
    dataPlayer = data[0]
    dataEnemy = data[1]
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#181864')
    ax.set_facecolor('#181864')
    ax.plot(dataPlayer[0], dataPlayer[1], label="Selected player")
    ax.plot(dataEnemy[0], dataEnemy[1], c='r', label="Enemy laner")
    x = numpy.array(dataPlayer[0])
    y = numpy.array(dataPlayer[1])
    enemy = numpy.array(dataEnemy[1])
    ax.fill_between(x, y, enemy, where=(y > enemy), color='#00FFFF', alpha=0.2, interpolate=True)
    ax.fill_between(x, y, enemy, where=(y <= enemy), color='r', alpha=0.4, interpolate=True)
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Total Gold')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors="white")
    ax.legend()
    ax.grid()
    ax.set_title("Player Gold", color="white")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")

    return image_base64



if __name__ == "__main__":
    myPuuid = '0eVFsOl4yyzV538TUwDUo9qLISJ4fKosKDlpi0f8M_NoXluWsVF1hk-YSt21YjgV2C3GPXfjV1lwfw'
    username = "Naayil"
    tag = "666"
    myPuuid = getPuuid(username, tag)

    insertMatchesIntoFiles()
    # info -> participants[] -> championName
    # getMatchIds()
    if False:
        if False:
            challengers = getSummonersWithRank(ranks[0], rankDistributions[0])
            with open(f'{outputDirectory}/summoners.json', 'w') as f:
                json.dump(challengers, f)

            matchSet = set()
            for challenger in challengers:
                matchIds = getMatchIds(challenger)
                for id in matchIds:
                    matchSet.add(id)

            with open(f'{outputDirectory}/matchIds.json', 'w') as f:
                json.dump(list(matchSet), f)

            print(len(matchSet))
        else:
            input_file = open (f'{outputDirectory}/matchIds.json')
            json_array = json.load(input_file)
            store_list = []

            for item in json_array:
                print(item)
            input_file.close()


    else:
        if True:
            pass
        else:
            getKillsFromHistory()

def getParticipantIdInMatch(puuid, match):
    participants = match["metadata"]["participants"]
    return participants.index(puuid)