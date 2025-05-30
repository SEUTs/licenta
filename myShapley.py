from itertools import permutations
import numpy as np
import json

with open("samples\\sampleReduced.json", 'r') as f:
    soloData = json.load(f)
    f.close()
with open("samples\\sampleTeammatesReduced.json", 'r') as f:
    duoData = json.load(f)
    f.close()
with open("samples\\sampleEnemiesReduced.json", 'r') as f:
    versusData = json.load(f)
    f.close()
gameMinimum = 0
    
def soloWinrate(champion):
    wins = soloData[champion][0]["wins"] + soloData[champion][1]["wins"] + soloData[champion][2]["wins"]
    games = soloData[champion][0]["met"] + soloData[champion][1]["met"] + soloData[champion][2]["met"]
    
    if games > gameMinimum:
        return wins / games
    return None

def duoWinrate(pair):
    if duoData.get(pair[0], {}).get(pair[1]) is not None:
        wins = duoData[pair[0]][pair[1]]["wins"]
        met = duoData[pair[0]][pair[1]]["met"]
        if met > gameMinimum:
            return wins / met
        return None
    return None

def versusWinrate(pair):
    if pair[1] == "Cappa":
        return 0.5
    if versusData.get(pair[0], {}).get(pair[1]) is not None:
        wins = versusData[pair[0]][pair[1]]["wins"]
        met = versusData[pair[0]][pair[1]]["met"]
        if met > gameMinimum:
            return wins / met
        return None
    return None

def withoutWinrate(pair, champion):
    wins = soloData[champion][0]["wins"] + soloData[champion][1]["wins"] + soloData[champion][2]["wins"]
    met = soloData[champion][0]["met"] + soloData[champion][1]["met"] + soloData[champion][2]["met"]
    
    if duoData.get(pair[0], {}).get(pair[1]) is not None:
        wins -= duoData[pair[0]][pair[1]]["wins"]
        met -= duoData[pair[0]][pair[1]]["met"]

        if met > gameMinimum:
            return wins / met
        return None

def shapley_value_team(champion, team):
    marginal_contribs = [soloWinrate(champion) - 0.5]

    for champ in team:
        if champ == "Cappa":
            continue
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
    # print(marginal_contribs)
    return round(np.mean(marginal_contribs) * 100, 2)

def shapley_value_enemies(champion, team):
    marginal_contribs = [soloWinrate(champion) - 0.5]

    for champ in team:
        if champ == "Cappa":
            continue
        if champ == champion:
            continue
        
        # without = withoutWinrate([champ, champion], champ)
        without = soloWinrate(champ)
        if without is None:
            continue

        with_champion = versusWinrate([champion, champ])
        if with_champion is None:
            continue

        marginal_contribs.append(with_champion - without)
    # print(marginal_contribs)
    return round(np.mean(marginal_contribs) * 100, 2)




toplaners = ['Aatrox', 'Akali', 'Ambessa', 'Aurora', 'Camille', 'Cassiopeia', "Cho'Gath", 'Darius', 'Dr._Mundo', 'Fiora', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Gwen', 'Heimerdinger', 'Illaoi', 'Irelia', 'Jax', 'Jayce', "K'Sante", 'Kayle', 'Kennen', 'Kled', 'Malphite', 'Mordekaiser', 'Nasus', 'Nidalee', 'Olaf', 'Ornn', 'Pantheon', 'Poppy', 'Quinn', 'Renekton', 'Riven', 'Rumble', 'Ryze', 'Sett', 'Shen', 'Singed', 'Sion', 'Smolder', 'Sylas', 'Tahm_Kench', 'Teemo', 'Trundle', 'Tryndamere', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Vladimir', 'Volibear', 'Warwick', 'Wukong', 'Yasuo', 'Yone', 'Yorick', 'Zac']
junglers = ['Amumu', "Bel'Veth", 'Briar', 'Diana', 'Dr._Mundo', 'Ekko', 'Elise', 'Evelynn', 'Fiddlesticks', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Ivern', 'Jarvan_IV', 'Jax', 'Karthus', 'Kayn', "Kha'Zix", 'Kindred', 'Lee_Sin', 'Lillia', 'Master_Yi', 'Naafiri', 'Nidalee', 'Nocturne', 'Nunu', 'Pantheon', 'Poppy', 'Qiyana', 'Rammus', "Rek'Sai", 'Rengar', 'Sejuani', 'Shaco', 'Shyvana', 'Skarner', 'Taliyah', 'Talon', 'Trundle', 'Udyr', 'Vi', 'Viego', 'Volibear', 'Warwick', 'Wukong', 'Xin_Zhao', 'Zac', 'Zed', 'Zyra']
midlaners = ['Ahri', 'Akali', 'Akshan', 'Anivia', 'Annie', 'Aurelion_Sol', 'Aurora', 'Azir', 'Cassiopeia', "Cho'Gath", 'Corki', 'Diana', 'Ekko', 'Fizz', 'Galio', 'Gragas', 'Hwei', 'Irelia', 'Jayce', 'Kassadin', 'Katarina', 'Kayle', 'Kennen', 'LeBlanc', 'Lissandra', 'Lux', 'Malphite', 'Malzahar', 'Mel', 'Naafiri', 'Neeko', 'Orianna', 'Pantheon', 'Qiyana', 'Ryze', 'Sion', 'Smolder', 'Swain', 'Sylas', 'Syndra', 'Taliyah', 'Talon', 'Tristana', 'Twisted_Fate', 'Veigar', "Vel'Koz", 'Vex', 'Viktor', 'Vladimir', 'Xerath', 'Yasuo', 'Yone', 'Zed', 'Zoe']
botlaners = ['Aphelios', 'Ashe', 'Caitlyn', 'Corki', 'Draven', 'Ezreal', 'Hwei', 'Jhin', 'Jinx', "Kai'Sa", 'Kalista', "Kog'Maw", 'Lucian', 'Lux', 'Mel', 'Miss_Fortune', 'Nilah', 'Samira', 'Senna', 'Seraphine', 'Sivir', 'Smolder', 'Swain', 'Tristana', 'Twitch', 'Varus', 'Vayne', 'Xayah', 'Yasuo', 'Zeri', 'Ziggs']
supports = ['Alistar', 'Annie', 'Ashe', 'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Elise', 'Fiddlesticks', 'Galio', 'Hwei', 'Janna', 'Karma', 'LeBlanc', 'Leona', 'Lulu', 'Lux', 'Maokai', 'Mel', 'Milio', 'Morgana', 'Nami', 'Nautilus', 'Neeko', 'Nidalee', 'Pantheon', 'Poppy', 'Pyke', 'Rakan', 'Rell', 'Renata_Glasc', 'Senna', 'Seraphine', 'Shaco', 'Shen', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Tahm_Kench', 'Taric', 'Thresh', "Vel'Koz", 'Xerath', 'Yuumi', 'Zilean', 'Zoe', 'Zyra']
championPools = [toplaners, junglers, midlaners, botlaners, supports]

def getChampions(role):
    return championPools[role]




def getBestChampions(role, team, enemies, ratios):
    shapleyDict = {}
    divider = sum(ratios)
    if divider == 0:
        return

    pool = championPools[role]
    for champion in pool:
        if champion in enemies:
            continue 

        shapleyScore = 0
        if ratios[0] != 0:
            teamShapley = shapley_value_team(champion, team).item()
            shapleyScore += teamShapley * ratios[0]
        if ratios[1] != 0:
            # print(champion, enemies[role])
            lanerShapley = round((versusWinrate([champion, enemies[role]]) - soloWinrate(champion)) * 100, 2)
            shapleyScore += lanerShapley * ratios[1]
        if ratios[2] != 0:
            enemyShapley = shapley_value_enemies(champion, enemies).item()
            shapleyScore += enemyShapley * ratios[2]
        if shapleyScore >= 0:
            shapleyScore /= divider
            # print(f"{champion}: {teamShapley, lanerShapley, enemyShapley, shapleyScore}")
            shapleyDict.update({champion: round(shapleyScore, 2)})
    
    return sorted(shapleyDict.items(), key=lambda item: -item[1])


if __name__ == "__main__":
    # team = ['Dr._Mundo', 'Warwick', 'Syndra', 'Ezreal', 'Yuumi']
    team = ["Cappa", "Jax", "Annie", "Ashe", "Blitzcrank"]
    enemies = ["Cho'Gath", "Nidalee", "Syndra", "Jhin", "Pyke"]
    print(getBestChampions(0, team, enemies, (1, 1, 1)))