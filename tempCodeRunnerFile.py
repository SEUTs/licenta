import json
with open("samples\\sampleReduced.json", 'r') as f:
    data = json.load(f)
    f.close()
    count = 0
    for champ in data:
        count += data[champ][0]['met'] + data[champ][1]['met'] + data[champ][2]['met']
print(count // 10)