import json

with open("items.json", 'r') as itemsFile, open("itemStats.json", 'r') as itemStatsFile:
    items = json.load(itemsFile)
    itemsFile.close()
    
    itemStats = json.load(itemStatsFile)
    itemStatsFile.close()

    for item in items.values():
        if item not in itemStats:
            print(item)