from os import listdir
import json

result = {}

files = listdir("samples\\masteries")
for file in files:
    with open("samples\\masteries\\" + file, 'r') as f:
        data = json.load(f)
        f.close()
    
    masteries = data["masteries"]
    # total = sum(masteries.values())
    
    champ1Range = min(5, len(masteries))
    
    currChamp = 0
    for champ1 in masteries:
        
        value1 = masteries[champ1]
        # if value1 < 20000:
        #     break
        currChamp += 1
        if currChamp > champ1Range:
            break
        
        forChamp1 = result.get(champ1, {})
        analyzed = forChamp1.get("found", 0)
        analyzed += 1
        forChamp1.update({"found": analyzed})
        
        for champ2 in masteries:
            if champ1 == champ2:
                continue
            
            value2 = masteries[champ2]
            if value2 == 0:
                break
            
            forChamp2 = forChamp1.get(champ2, [])
            forChamp2.append(value2 / value1 * 100)
            forChamp1.update({champ2: forChamp2})
        result.update({champ1: forChamp1})
            # if value < 20000:
            #     break
            # print(f"{champ}: {value}/{total} ({round(value / total * 100, 2)})")

print(str(result["Aatrox"]["Darius"]) + "\n\n")
print(str(result["Aatrox"]["Hwei"]) + "\n\n")
print(str(result["Aatrox"]["LeBlanc"]) + "\n\n")
print(str(result["Aatrox"]["Volibear"]) + "\n\n")
for champ1 in result:
    for champ2 in result[champ1]:
        if champ2 == "found":
            continue
        print(champ2, result[champ1][champ2])
        statistics = sorted(result[champ1][champ2])
        sampleSize = len(statistics)
        result[champ1].update({champ2: [statistics[sampleSize // 2], sampleSize]})


with open("result.json", 'w+') as f:
    json_object = json.dumps(result, indent=4)
    print(len(json_object))
    f.write(json_object)
    f.close()