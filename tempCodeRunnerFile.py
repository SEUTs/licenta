import json
with open("result.json", 'r') as f:
    data = json.load(f)
    f.close()

toplaners = ['Aatrox', 'Akali', 'Ambessa', 'Aurora', 'Camille', 'Cassiopeia', "Cho'Gath", 'Darius', 'Dr._Mundo', 'Fiora', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Gwen', 'Heimerdinger', 'Illaoi', 'Irelia', 'Jax', 'Jayce', "K'Sante", 'Kayle', 'Kennen', 'Kled', 'Malphite', 'Mordekaiser', 'Nasus', 'Nidalee', 'Olaf', 'Ornn', 'Pantheon', 'Poppy', 'Quinn', 'Renekton', 'Riven', 'Rumble', 'Ryze', 'Sett', 'Shen', 'Singed', 'Sion', 'Smolder', 'Sylas', 'Tahm_Kench', 'Teemo', 'Trundle', 'Tryndamere', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Vladimir', 'Volibear', 'Warwick', 'Wukong', 'Yasuo', 'Yone', 'Yorick', 'Zac']
junglers = ['Amumu', "Bel'Veth", 'Briar', 'Diana', 'Dr._Mundo', 'Ekko', 'Elise', 'Evelynn', 'Fiddlesticks', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Ivern', 'Jarvan_IV', 'Jax', 'Karthus', 'Kayn', "Kha'Zix", 'Kindred', 'Lee_Sin', 'Lillia', 'Master_Yi', 'Naafiri', 'Nidalee', 'Nocturne', 'Nunu', 'Pantheon', 'Poppy', 'Qiyana', 'Rammus', "Rek'Sai", 'Rengar', 'Sejuani', 'Shaco', 'Shyvana', 'Skarner', 'Taliyah', 'Talon', 'Trundle', 'Udyr', 'Vi', 'Viego', 'Volibear', 'Warwick', 'Wukong', 'Xin_Zhao', 'Zac', 'Zed', 'Zyra']
midlaners = ['Ahri', 'Akali', 'Akshan', 'Anivia', 'Annie', 'Aurelion_Sol', 'Aurora', 'Azir', 'Cassiopeia', "Cho'Gath", 'Corki', 'Diana', 'Ekko', 'Fizz', 'Galio', 'Gragas', 'Hwei', 'Irelia', 'Jayce', 'Kassadin', 'Katarina', 'Kayle', 'Kennen', 'LeBlanc', 'Lissandra', 'Lux', 'Malphite', 'Malzahar', 'Mel', 'Naafiri', 'Neeko', 'Orianna', 'Pantheon', 'Qiyana', 'Ryze', 'Sion', 'Smolder', 'Swain', 'Sylas', 'Syndra', 'Taliyah', 'Talon', 'Tristana', 'Twisted_Fate', 'Veigar', "Vel'Koz", 'Vex', 'Viktor', 'Vladimir', 'Xerath', 'Yasuo', 'Yone', 'Zed', 'Zoe']
botlaners = ['Aphelios', 'Ashe', 'Caitlyn', 'Corki', 'Draven', 'Ezreal', 'Hwei', 'Jhin', 'Jinx', "Kai'Sa", 'Kalista', "Kog'Maw", 'Lucian', 'Lux', 'Mel', 'Miss_Fortune', 'Nilah', 'Samira', 'Senna', 'Seraphine', 'Sivir', 'Smolder', 'Swain', 'Tristana', 'Twitch', 'Varus', 'Vayne', 'Xayah', 'Yasuo', 'Zeri', 'Ziggs']
supports = ['Alistar', 'Annie', 'Ashe', 'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Elise', 'Fiddlesticks', 'Galio', 'Hwei', 'Janna', 'Karma', 'LeBlanc', 'Leona', 'Lulu', 'Lux', 'Maokai', 'Mel', 'Milio', 'Morgana', 'Nami', 'Nautilus', 'Neeko', 'Nidalee', 'Pantheon', 'Poppy', 'Pyke', 'Rakan', 'Rell', 'Renata_Glasc', 'Senna', 'Seraphine', 'Shaco', 'Shen', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Tahm_Kench', 'Taric', 'Thresh', "Vel'Koz", 'Xerath', 'Yuumi', 'Zilean', 'Zoe', 'Zyra']
championPools = [toplaners, junglers, midlaners, botlaners, supports]

def getAlsoPlayed(champion):
    yoneData = data[champion].copy()
    found = yoneData["found"]
    yoneData.pop("found")
    output = dict(sorted(yoneData.items(), key=lambda item: -item[1][0]))

    alsoPlayed = []
    for pool in championPools:
        alsoPlayed.append(dict([[x, round(output[x][1] / found * 100, 2)] for x in output if x in pool and output[x][1] / found > 0.75]))
    return alsoPlayed
getAlsoPlayed("Yone")