from itertools import permutations
import numpy as np
import json

with open("samples\\sampleReduced.json", 'r') as f:
    soloData = json.load(f)
    f.close()
with open("samples\\sampleTeammatesReduced.json", 'r') as f:
    duoData = json.load(f)
    f.close()
    
def soloWinrate(champion):
    wins = soloData[champion][0]["wins"] + soloData[champion][1]["wins"] + soloData[champion][2]["wins"]
    games = soloData[champion][0]["met"] + soloData[champion][1]["met"] + soloData[champion][2]["met"]
    
    if games > 80:
        return wins / games
    return None

def duoWinrate(pair):
    if duoData.get(pair[0], {}).get(pair[1]) is not None:
        wins = duoData[pair[0]][pair[1]]["wins"]
        met = duoData[pair[0]][pair[1]]["met"]
        if met > 80:
            return wins / met
        return None
    return None

def withoutWinrate(pair, champion):
    wins = soloData[champion][0]["wins"] + soloData[champion][1]["wins"] + soloData[champion][2]["wins"]
    met = soloData[champion][0]["met"] + soloData[champion][1]["met"] + soloData[champion][2]["met"]
    
    if duoData.get(pair[0], {}).get(pair[1]) is not None:
        wins -= duoData[pair[0]][pair[1]]["wins"]
        met -= duoData[pair[0]][pair[1]]["met"]

        if met > 80:
            return wins / met
        return None

def shapley_value(champion, team):
    marginal_contribs = [soloWinrate(champion) - 0.5]

    for champ in team:
        if champ == champion:
            continue
        
        # without = withoutWinrate([champ, champion], champ)
        without = soloWinrate(champ)
        if without is None:
            continue

        with_champion = duoWinrate([champ, champion])
        if with_champion is None:
            continue

        marginal_contribs.append(with_champion - without)
    print(marginal_contribs)
    return (round(marginal_contribs[0] * 100 + 50, 2), round(np.mean(marginal_contribs) * 100, 2))

if __name__ == "__main__":
    team = ['Dr._Mundo', 'Warwick', 'Syndra', 'Ezreal', 'Yuumi']
    print(shapley_value("Dr._Mundo", team))