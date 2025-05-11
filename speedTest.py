import json
import os
import extractData
import time
import matplotlib as plt
import getMatchData

dir_path = r'E:\\licenta\\games'
def cleanFiles():
    start = time.time()
    for file in os.listdir(dir_path):
        with open(dir_path + '\\' + file, 'r') as f:
            data = json.load(f)
            f.close()
            if "httpStatus" in data:
                os.remove(dir_path + '\\' + file)
            # if data["info"]["frames"][-1]["timestamp"] < 240000:
            #     print(file + " " + "deleted for beign too short")
            #     os.remove(dir_path + '\\' + file)
    print(time.time() - start)

# getDeathStats()

def getGoldPerMinute(playerIndex, matchFile): 
    with open(matchFile, 'r') as f:
        data = json.load(f)
        f.close()
        frames = data["info"]["frames"]
        for frame in frames:
            championStats = frame["participantFrames"]
            print(championStats[playerIndex]["totalGold"])
            
    
if __name__ == "__main__":
    deathStats = getMatchData.getDeathStats()
    for player in deathStats:
        print("\n\n")
        print(deathStats[player])
    # cleanFiles()
    # file = os.listdir(dir_path)[0]
    # getGoldPerMinute('1', dir_path + '\\' + file)