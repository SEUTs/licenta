import json
from os import listdir

files = listdir("D:\\licenta\\reducedGames")
allData = {}

curr = 0
total = str(len(files))

for file in files:
    curr += 1
    with open("D:\\licenta\\reducedGames\\" + file) as f:
        data = json.load(f)
        f.close()
    allData.update({file: data})
    print(str(curr) + '/' + total)
    
with open("D:\\licenta\\reducedMotherload.json") as f:
    json_object = json.dumps(allData, indent=4)
    f.write(json_object)
    f.close()