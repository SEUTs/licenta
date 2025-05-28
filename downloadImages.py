import requests
import json

def getChampions():
    with open('samples\\sampleReduced.json', 'r') as f:
        data = json.load(f)
        f.close()
        for champ in data:
            data = requests.get(f'https://wiki.leagueoflegends.com/en-us/images/thumb/{champ}_OriginalSquare.png/70px-{champ}_OriginalSquare.png?54659.png.webp').content
            f = open('static\\icons\\champions\\' + champ + '.jpg','wb')
            f.write(data)
            f.close()

def getItems():
    #TODO: NOT DONE
    with open('samples\\sampleReduced.json', 'r') as f:
        data = json.load(f)
        f.close()
        for champ in data:
            data = requests.get(f'https://wiki.leagueoflegends.com/en-us/images/thumb/{champ}_OriginalSquare.png/70px-{champ}_OriginalSquare.png?54659.png.webp').content
            f = open('static\\icons\\champions\\' + champ + '.jpg','wb')
            f.write(data)
            f.close()

if __name__ == "__main__":
    pass