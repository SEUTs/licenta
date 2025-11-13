import json
import licenta
from time import time
import matplotlib.pyplot as plt
from os.path import isfile

def getMasteries(credentials, region):
    def getUsefulMasteriesFormat(rawMasteryData):
        with open("champions.json", 'r') as f:
            championNames = json.load(f)
            f.close()
            
        usefulMasteryData = {}
        for champion in rawMasteryData:
            usefulMasteryData.update({championNames[str(champion["championId"])]: champion["championPoints"]})
        return usefulMasteryData
    
    if type(credentials) == list:
        with open("puuids.json", 'r') as f:
            puuidData = json.load(f)
            f.close()
            puuid = puuidData.get(credentials[0] + '#' + credentials[1])
            if puuid is None:
                puuid = licenta.getPuuid(credentials[0], credentials[1])
    else:
        puuid = credentials
        
    filePath = "samples\\masteries\\" + puuid + ".json"
    currTime = int(time())
    
    if isfile(filePath):
        with open(filePath, 'r') as f:
            data = json.load(f)
            f.close()
        
        if currTime - data["timestamp"] < 864000: # 10 days
            return data["masteries"]
        
    newMasteries = getUsefulMasteriesFormat(licenta.getChampionMastery(puuid, region))
    json_object = json.dumps({"timestamp" : currTime, "masteries": newMasteries})
    with open(filePath, 'w+') as f:
        f.write(json_object)
        f.close()
    return newMasteries

# def getMasteries(username = "saseunticnit", tagLine="seuts", region="eun"):
#     def getUserTime(user):
#         with open("storedFor.json", 'r') as f:
#             data = json.load(f)
#             f.close()
#         return data.get(user)

#     def addUserTime(user):
#         with open("storedFor.json", 'r') as f:
#             data = json.load(f)
#             f.close()
#         with open("storedFor.json", 'w') as f:
#             userTime = int(time())
#             data.update({user: userTime})
#             json_object = json.dumps(data, indent=4)
#             f.write(json_object)
#             f.close()

    

#     username = username.lower()
#     tagLine = tagLine.lower()
#     user = f"{username}#{tagLine}"
#     with open("puuids.json", 'r') as f:
#         data = json.load(f)
#         f.close()
#         puuid = data.get(user)
#         if puuid is None:
#             puuid = licenta.getPuuid(username, tagLine)
#             data.update({user: puuid})
#             json_object = json.dumps(data, indent=4)
#             with open("puuids.json", 'w') as f:
#                 f.write(json_object)
#                 f.close()

#     userTime = getUserTime(user)
#     if userTime is not None:
#         if time() - userTime < 864000: # 10 days
#             with open("samples\\masteries\\" + user + ".json", 'r') as g:
#                 usefulMasteryData = json.load(g)
#                 g.close()
#                 return usefulMasteryData
#         else:
#             operation = 'w'
#     else:
#         operation = 'x'

#     with open("samples\\masteries\\" + user + ".json", operation) as f:
#         rawMasteryData = licenta.getChampionMastery(puuid, region)
#         usefulMasteryData = getUsefulMasteryData(rawMasteryData)
#         json_object = json.dumps(usefulMasteryData, indent=4)
#         f.write(json_object)
#         f.close()
#     addUserTime(user)
#     return usefulMasteryData

# def getMasteriesWithPuuid(puuid, region="eun"):
#     def getUserTime(puuid):
#         with open("storedFor.json", 'r') as f:
#             data = json.load(f)
#             f.close()
#         return data.get(puuid)

#     def addUserTime(puuid):
#         with open("storedFor.json", 'r') as f:
#             data = json.load(f)
#             f.close()
#         with open("storedFor.json", 'w') as f:
#             userTime = int(time())
#             data.update({puuid: userTime})
#             json_object = json.dumps(data, indent=4)
#             f.write(json_object)
#             f.close()

#     def getUsefulMasteryData(rawMasteryData):
#         with open("champions.json", 'r') as f:
#             championNames = json.load(f)
#             f.close()
            
#         usefulMasteryData = {}
#         for champion in rawMasteryData:
#             usefulMasteryData.update({championNames[str(champion["championId"])]: champion["championPoints"]})
#         return usefulMasteryData

#     userTime = getUserTime(puuid)
#     if userTime is not None:
#         if time() - userTime < 864000: # 10 days
#             with open("samples\\masteries\\" + puuid + ".json", 'r') as g:
#                 usefulMasteryData = json.load(g)
#                 g.close()
#                 return usefulMasteryData
#         else:
#             operation = 'w'
#     else:
#         operation = 'x'

#     with open("samples\\masteries\\" + puuid + ".json", operation) as f:
#         rawMasteryData = licenta.getChampionMastery(puuid, region)
#         usefulMasteryData = getUsefulMasteryData(rawMasteryData)
#         json_object = json.dumps(usefulMasteryData, indent=4)
#         f.write(json_object)
#         f.close()
#     addUserTime(puuid)
#     return usefulMasteryData

def getTop5Champs(credentials, region):
    masteries = getMasteries(credentials, region)
    result = []
    i = 0
    for champ in masteries:
        if champ == "Yunara":
            continue
        result.append([champ, masteries[champ]])
        i += 1
        if i == 5:
            return result
        
def getTopNChamps(credentials, region, N):
    masteries = getMasteries(credentials, region)
    result = []
    i = 0
    for champ in masteries:
        if champ == "Yunara":
            continue
        result.append([champ, masteries[champ]])
        i += 1
        if i == N:
            return result
    return result

def getTop5ChampsAndTotalMasteries(credentials, region):
    masteries = getMasteries(credentials, region)
    champs = []
    i = 0
    for champ in masteries:
        if champ == "Yunara":
            continue
        champs.append([champ, masteries[champ]])
        i += 1
        if i == 5:
            break
    result = [champs, sum(masteries.values())]
    return result

def getSkills(credentials, region):
    masteries = getMasteries(credentials, region)
    skills = {}
    with open("championCharacteristics.json", 'r') as f:
        championData = json.load(f)
        f.close()

    for champ in masteries:
        data = championData[champ]
        amplifier = masteries[champ] # // 500

        currDiff = skills.get("difficulties", {"1": 0, "2": 0, "3": 0})
        currDiff.update({data["difficulty"]: currDiff[data["difficulty"]] + amplifier})
        skills.update({"difficulties": currDiff})

        currPlaystyles = skills.get("playstyles", {})
        thisChampPlaystyle = int(data["playstyle"])
        playstyle = "Basic" if thisChampPlaystyle < 25 else "Mixed" if thisChampPlaystyle < 75 else "Ability"
        currPlaystyles.update({playstyle: currPlaystyles.get(playstyle, 0) + amplifier})
        skills.update({"playstyles": currPlaystyles})

        currClasses = skills.get("classes", {})
        for c in data["classes"]:
            cExp = currClasses.get(c, 0)
            currClasses.update({c: cExp + amplifier})
        skills.update({"classes": currClasses})

        currRanges = skills.get("ranges", {})
        range = data["range"]
        currRanges.update({range: currRanges.get(range, 0) + amplifier})
        skills.update({"ranges": currRanges})


        values = data["values"]
        skillValues = skills.get("values", {})

        
        currDamage = skillValues.get("damage", {})
        skillDamageValues = currDamage.get("values", {"1": 0, "2": 0, "3": 0})
        skillDamageValues.update({values["damage"]["value"]: skillDamageValues.get(values["damage"]["value"], 0) + amplifier})
        currDamage.update({"values": skillDamageValues})
        skillDamageDuration = currDamage.get("duration", {"Burst": 0, "DPS": 0})
        skillDamageDuration.update({values["damage"]["duration"]: skillDamageDuration.get(values["damage"]["duration"], 0) + amplifier})
        currDamage.update({"duration": skillDamageDuration})
        skillDamageType = currDamage.get("damageType", {"Physical": 0, "Hybrid": 0, "Magic": 0})
        skillDamageType.update({values["damage"]["damageType"]: skillDamageType.get(values["damage"]["damageType"], 0) + amplifier})
        currDamage.update({"damageType": skillDamageType})
        skillDamageTarget = currDamage.get("damageTarget", {"Single": 0, "Multiple": 0})
        skillDamageTarget.update({values["damage"]["damageTarget"]: skillDamageTarget.get(values["damage"]["damageTarget"], 0) + amplifier})
        currDamage.update({"damageTarget": skillDamageTarget})
        
        currToughness = skillValues.get("toughness", {})
        skillToughnessValues = currToughness.get("values", {"1": 0, "2": 0, "3": 0})
        skillToughnessValues.update({values["toughness"]["value"]: skillToughnessValues.get(values["toughness"]["value"], 0) + amplifier})
        currToughness.update({"values": skillToughnessValues})
        skillToughnessType = currToughness.get("toughnessType", {"Burst": 0, "Sustained": 0})
        skillToughnessType.update({values["toughness"]["toughnessType"]: skillToughnessType.get(values["toughness"]["toughnessType"], 0) + amplifier})
        currToughness.update({"toughnessType": skillToughnessType})
        
        currControl = skillValues.get("control", {})
        skillControlValues = currControl.get("values", {"0": 0, "1": 0, "2": 0, "3": 0})
        skillControlValues.update({values["control"]["value"]: skillControlValues.get(values["control"]["value"], 0) + amplifier})
        currControl.update({"values": skillControlValues})
        skillControlTarget = currControl.get("controlTarget", {"Single": 0, "Multiple": 0, "Mixed": 0})
        skillControlTarget.update({values["control"]["controlTarget"]: skillControlTarget.get(values["control"]["controlTarget"], 0) + amplifier})
        currControl.update({"controlTarget": skillControlTarget})

        currMobility = skillValues.get("mobility", {})
        skillMobilityValue = currMobility.get("values", {"0": 0, "1": 0, "2": 0, "3": 0})
        skillMobilityValue.update({values["mobility"]["value"]: skillMobilityValue.get(values["mobility"]["value"], 0) + amplifier})
        currMobility.update({"values": skillMobilityValue})
        currMobilityType = currMobility.get("mobilityType", {"Burst": 0, "Sustained": 0})
        currMobilityType.update({values["mobility"]["mobilityType"]: currMobilityType.get(values["mobility"]["mobilityType"], 0) + amplifier})
        currMobility.update({"mobilityType": currMobilityType})

        currUtility = skillValues.get("utility", {})
        skillUtilityValue = currUtility.get("values", {"0": 0, "1": 0, "2": 0, "3": 0})
        skillUtilityValue.update({values["utility"]["value"]: skillUtilityValue.get(values["utility"]["value"], 0) + amplifier})
        currUtility.update({"values": skillUtilityValue})

        skillValues.update({"damage": currDamage})
        skillValues.update({"toughness": currToughness})
        skillValues.update({"control": currControl})
        skillValues.update({"mobility": currMobility})
        skillValues.update({"utility": currUtility})
        skills.update({"values": skillValues})


    return skills

if __name__ == "__main__":
    skills = getSkills(["bianca", "nya"], "eun")
    print(skills)

    plt.rcParams['font.size'] = 8
    plt.subplot(3, 5, 1)
    plt.title("Champion difficulties", fontsize=10)
    plt.pie(skills["difficulties"].values(), labels=skills["difficulties"].keys())
    plt.subplot(3, 5, 2)
    plt.title("Champion playstyles", fontsize=10)
    plt.pie(skills["playstyles"].values(), labels=skills["playstyles"].keys())
    plt.subplot(3, 5, 3)
    plt.title("Champion classes", fontsize=10)
    plt.pie(skills["classes"].values(), labels=skills["classes"].keys())
    plt.subplot(3, 5, 4)
    plt.title("Champion ranges", fontsize=10)
    plt.pie(skills["ranges"].values(), labels=skills["ranges"].keys())
    plt.subplot(3, 5, 5)
    plt.title("Champion damage", fontsize=10)
    plt.pie(skills["values"]["damage"]["values"].values(), labels=["low", "medium", "high"])
    plt.subplot(3, 5, 6)
    plt.title("Champion damage", fontsize=10)
    plt.pie(skills["values"]["damage"]["duration"].values(), labels=skills["values"]["damage"]["duration"].keys())
    plt.subplot(3, 5, 7)
    plt.title("Champion damage", fontsize=10)
    plt.pie(skills["values"]["damage"]["damageType"].values(), labels=skills["values"]["damage"]["damageType"].keys())
    plt.subplot(3, 5, 8)
    plt.title("Damage targets", fontsize=10)
    plt.pie(skills["values"]["damage"]["damageTarget"].values(), labels=skills["values"]["damage"]["damageTarget"].keys())
    plt.subplot(3, 5, 9)
    plt.title("Champion tankiness", fontsize=10)
    plt.pie(skills["values"]["toughness"]["values"].values(), labels=skills["values"]["toughness"]["values"].keys())
    plt.subplot(3, 5, 10)
    plt.title("Champion tankiness types", fontsize=10)
    plt.pie(skills["values"]["toughness"]["toughnessType"].values(), labels=skills["values"]["toughness"]["toughnessType"].keys())
    plt.subplot(3, 5, 11)
    plt.title("Champion cc", fontsize=10)
    plt.pie(skills["values"]["control"]["values"].values(), labels=["none", "low", "medium", "high"])
    plt.subplot(3, 5, 12)
    plt.title("Champion cc target", fontsize=10)
    plt.pie(skills["values"]["control"]["controlTarget"].values(), labels=skills["values"]["control"]["controlTarget"].keys())
    plt.subplot(3, 5, 13)
    plt.title("Champion mobility", fontsize=10)
    plt.pie(skills["values"]["mobility"]["values"].values(), labels=["none", "low", "medium", "high"])
    plt.subplot(3, 5, 14)
    plt.title("Champion mobility", fontsize=10)
    plt.pie(skills["values"]["mobility"]["mobilityType"].values(), labels=skills["values"]["mobility"]["mobilityType"].keys())
    plt.subplot(3, 5, 15)
    plt.title("Champion utility", fontsize=10)
    plt.pie(skills["values"]["utility"]["values"].values(), labels=["none", "low", "medium", "high"])
    plt.show()

    # sorteaza sampleReduced si teammates si enemies