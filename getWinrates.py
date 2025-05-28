import json
import os
import extractData
import threading

dir_path = r'E:\\licenta\\games'
def byHours():
    wins = {}
    met = {}
    scanned = 0
    files = os.listdir(dir_path)
    toScan = len(files)
    for file in files:
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
                
        print(f"{scanned} / {toScan}")
    result = {}

    for champion in met:
        entries = []
        for hour in range(0, 24, 8):
            entry = {"hour": hour, "wins": wins.get(champion, {}).get(hour, 0), "games": met.get(champion, {}).get(hour, 0)}
            entries.append(entry)
        result.update({champion: entries})

    # result.sort(key=lambda element: element[2]/element[3])
    
    for champion in result:
        print(champion, result[champion])
        # print(f"{element[0]} ({element[1]}): {element[2]} / {element[3]}")
    
    json_object = json.dumps(result, indent=4)
    
    with open("samples\\sample.json", "w") as outfile:
        outfile.write(json_object)
def byHoursReduced(part, total, displayProgress = False):
    print("Thread" + str(part) + " started")
    result = {}
    scanned = 0
    files = os.listdir("E:\\licenta\\reducedGames")
    toScan = len(files) // total
    files = files[(part - 1) * toScan : part * toScan]
    for file in files:
        with open('E:\\licenta\\reducedGames\\' + file, 'r') as f:
            reducedData = json.load(f)
            f.close()

            scanned += 1

            rts = reducedData.get("timestamp")
            hour = rts // 60 // 60 // 1000 % 24 // 8

            for champ in reducedData["winners"]:
                championStats = result.get(champ, [{"hour": 0, "wins": 0, "met": 0}, {"hour": 8, "wins": 0, "met": 0}, {"hour": 16, "wins": 0, "met": 0}])
                championStats[hour].update({"wins": championStats[hour]["wins"] + 1, "met": championStats[hour]["met"] + 1})
                result.update({champ: championStats})

            for champ in reducedData["losers"]:
                championStats = result.get(champ, [{"hour": 0, "wins": 0, "met": 0}, {"hour": 8, "wins": 0, "met": 0}, {"hour": 16, "wins": 0, "met": 0}])
                championStats[hour].update({"met": championStats[hour]["met"] + 1})
                result.update({champ: championStats})

        if displayProgress:
            print(f"{scanned} / {toScan}")
    
    json_object = json.dumps(result, indent=4)
    
    if os.path.isfile("samples\\sampleReduced" + str(part) + ".json"):
        with open("samples\\sampleReduced" + str(part) + ".json", "w") as outfile:
            outfile.write(json_object)
    else:
        with open("samples\\sampleReduced" + str(part) + ".json", "x") as outfile:
            outfile.write(json_object)


def byTeammates(part, total, displayProgress = False):
    result = {}
    scanned = 0
    files = os.listdir(dir_path)
    toScan = len(files) // total
    files = files[(part - 1) * toScan : part * toScan]
    for file in files:
        with open(dir_path + '\\' + file, 'r') as f:
            data = json.load(f)
            f.close()
            if data["info"]["frames"][-1]["timestamp"] < 240000:
                continue
            scanned += 1
            names = extractData.getChampionNames(data["info"]["frames"])
            winningTeam = extractData.getWinningTeam(data)
            for i in range((winningTeam-1) * 5, winningTeam * 5):
                championStats = result.get(names[i], {})
                for j in range((winningTeam-1) * 5, winningTeam * 5):
                    if i != j:
                        teammateStats = championStats.get(names[j], {"wins": 0, "met": 0})
                        teammateStats.update({"wins": teammateStats["wins"] + 1, "met": teammateStats["met"] + 1})
                        championStats.update({names[j]: teammateStats})
                result.update({names[i]: championStats})
            for i in range(10 - winningTeam * 5, 10 - (winningTeam-1) * 5):
                championStats = result.get(names[i], {})
                for j in range(10 - winningTeam * 5, 10 - (winningTeam-1) * 5):
                    if i != j:
                        teammateStats = championStats.get(names[j], {"wins": 0, "met": 0})
                        teammateStats.update({"met": teammateStats["met"] + 1})
                        championStats.update({names[j]: teammateStats})
                result.update({names[i]: championStats})

        if displayProgress:
            added = 0
            for champ in result:
                for mate in result[champ]:
                    added += result[champ][mate]["met"]
            # print(f"{scanned} / {toScan} : {added}")
            if added == 10000:
                print(result)
    
    json_object = json.dumps(result, indent=4)
    
    if os.path.isfile("samples\\sampleTeammates" + str(part) + ".json"):
        with open("samples\\sampleTeammates" + str(part) + ".json", "w") as outfile:
            outfile.write(json_object)
    else:
        with open("samples\\sampleTeammates" + str(part) + ".json", "x") as outfile:
            outfile.write(json_object)
def byTeammatesReduced(part, total, displayProgress = False):
    print("Thread" + str(part) + " started")
    result = {}
    scanned = 0
    files = os.listdir("E:\\licenta\\reducedGames")
    toScan = len(files) // total
    files = files[(part - 1) * toScan : part * toScan]
    for file in files:
        with open('E:\\licenta\\reducedGames\\' + file, 'r') as f:
            reducedData = json.load(f)
            f.close()

            scanned += 1

            for champ in reducedData["winners"]:
                championStats = result.get(champ, {})
                for teammate in reducedData["winners"]:
                    if champ != teammate:
                        teammateStats = championStats.get(teammate, {"wins": 0, "met": 0})
                        teammateStats.update({"wins": teammateStats["wins"] + 1, "met": teammateStats["met"] + 1})
                        championStats.update({teammate: teammateStats})
                result.update({champ: championStats})

            for champ in reducedData["losers"]:
                championStats = result.get(champ, {})
                for teammate in reducedData["losers"]:
                    if champ != teammate:
                        teammateStats = championStats.get(teammate, {"wins": 0, "met": 0})
                        teammateStats.update({"met": teammateStats["met"] + 1})
                        championStats.update({teammate: teammateStats})
                result.update({champ: championStats})

        if displayProgress:
            print(f"{scanned} / {toScan}")
    
    json_object = json.dumps(result, indent=4)
    
    if os.path.isfile("samples\\sampleTeammatesReduced" + str(part) + ".json"):
        with open("samples\\sampleTeammatesReduced" + str(part) + ".json", "w") as outfile:
            outfile.write(json_object)
    else:
        with open("samples\\sampleTeammatesReduced" + str(part) + ".json", "x") as outfile:
            outfile.write(json_object)

def useThreads():
    t1 = threading.Thread(target=byTeammates, args=(1,8,True))
    t2 = threading.Thread(target=byTeammates, args=(2,8,))
    t3 = threading.Thread(target=byTeammates, args=(3,8,))
    t4 = threading.Thread(target=byTeammates, args=(4,8,))
    t5 = threading.Thread(target=byTeammates, args=(5,8,))
    t6 = threading.Thread(target=byTeammates, args=(6,8,))
    t7 = threading.Thread(target=byTeammates, args=(7,8,))
    t8 = threading.Thread(target=byTeammates, args=(8,8,))

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True
    t5.daemon = True
    t6.daemon = True
    t7.daemon = True
    t8.daemon = True

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
def useThreadsReduced(target):
    t1 = threading.Thread(target=target, args=(1,8,True))
    t2 = threading.Thread(target=target, args=(2,8,))
    t3 = threading.Thread(target=target, args=(3,8,))
    t4 = threading.Thread(target=target, args=(4,8,))
    t5 = threading.Thread(target=target, args=(5,8,))
    t6 = threading.Thread(target=target, args=(6,8,))
    t7 = threading.Thread(target=target, args=(7,8,))
    t8 = threading.Thread(target=target, args=(8,8,))

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True
    t5.daemon = True
    t6.daemon = True
    t7.daemon = True
    t8.daemon = True

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()

def combineResults(forTeammates = False, forReduced = True):
    teammates = "Teammates" if forTeammates else ""
    reduced = "Reduced" if forReduced else ""

    fileTemplate = "samples\\sample" + teammates + reduced
    with open(f"{fileTemplate}1.json", 'r') as f:
        result = json.load(f)
        f.close()

    if forTeammates:
        for part in range(1, 9):
            with open(f"{fileTemplate}{part}.json", 'r') as f:
                data = json.load(f)
                f.close()
                for champion in data:
                    championData = result.get(champion, {})
                    for teammate in data[champion]:
                        beforeTeammate = championData.get(teammate, {"wins": 0, "met": 0})
                        print(part, teammate, beforeTeammate)
                        afterWins = beforeTeammate["wins"] + data[champion][teammate]["wins"]
                        afterMet = beforeTeammate["met"] + data[champion][teammate]["met"]
                        afterTeammate = {"wins": afterWins, "met": afterMet}
                        championData.update({teammate: afterTeammate})
                    result.update({champion: championData})

    else:
        for part in range(1, 9):
            with open(f"{fileTemplate}{part}.json", 'r') as f:
                data = json.load(f)
                f.close()
                for champion in data:
                    championStats = result.get(champion, [{"hour": 0, "wins": 0, "met": 0}, {"hour": 8, "wins": 0, "met": 0}, {"hour": 16, "wins": 0, "met": 0}])
                    for hour in range(3):
                        championStats[hour].update({
                            "wins": championStats[hour]["wins"] + data[champion][hour]["wins"],
                            "met": championStats[hour]["met"] + data[champion][hour]["met"]
                        })
                    result.update({champion: championStats})

    
    json_object = json.dumps(result, indent=4)
    
    with open(f"{fileTemplate}.json", 'w') as f:
        f.write(json_object)
        f.close()
    print("Done!")

if __name__ == "__main__":
    useThreadsReduced(target=byHoursReduced)
    combineResults(forTeammates=False, forReduced=True)