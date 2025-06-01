import json
import licenta

user = "SasEUnTicnit#seuts"
with open("puuids.json", 'r') as f:
    data = json.load(f)
    f.close()
    puuid = data.get(user)

with open("championMastery.json", 'w') as f:
    response = licenta.getChampionMastery(puuid)
    json_object = json.dumps(response, indent=4)
    f.write(json_object)
    f.close()

# sorteaza sampleReduced si teammates si enemies