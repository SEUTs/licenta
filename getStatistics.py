import json

def winrates(championName):
    winrates = []
    with open("samples\\sampleReduced.json", 'r') as f:
        data = json.load(f)
        f.close()
        championData = data.get(championName)
        if championData is not None:
            wins = [championData[i]["wins"] for i in range(3)]
            games = [championData[i]["met"] for i in range(3)]
            winrates.append(round(sum(wins)/sum(games) * 100, 2))

            for i in range(3):
                if games[i] != 0:
                    winrates.append(round(wins[i] / games[i] * 100, 2))
                else:
                    winrates.append(-1)
        else:
            winrates = (-1, -1, -1, -1)
    return winrates

def forTeammates(championName):
    with open("samples\\sampleTeammatesReduced.json", 'r') as f:
        champions = [championName]
        data = json.load(f)
        f.close()

        result = {}
        for champion in champions:
            for teammate in data[champion]:
                beforeTeammate = result.get(teammate, {"wins": 0, "met": 0})
                afterWins = beforeTeammate["wins"] + data[champion][teammate]["wins"]
                afterMet = beforeTeammate["met"] + data[champion][teammate]["met"]
                afterTeammate = {"wins": afterWins, "met": afterMet}
                result.update({teammate: afterTeammate})

        if "Cappa" in result:
            result.pop("Cappa")
        if championName in result:
            result.pop(championName)

        toPop = []
        for champ in result:
            if result[champ]["met"] < 80:
                toPop.append(champ)
        for next in toPop:
            result.pop(next)

        sortedByRatio = sorted(
            result.items(),
            key=lambda item: item[1]["wins"] / item[1]['met']
        )
        
        return sortedByRatio