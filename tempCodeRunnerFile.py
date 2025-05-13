import requests

def isGood(content):
    return not content.__contains__("NEXT_HTTP_ERROR_FALLBACK;404\\")

goodLink = "https://op.gg/lol/summoners/eune/SasEUnTicnit-SEUTs"
badLink = "https://op.gg/lol/summoners/eune/SasEUnTicnit2-SEUTs"

goodRequest = str(requests.get(goodLink).content)
badRequest = str(requests.get(badLink).content)

print(isGood(goodRequest))
print(isGood(badRequest))

# if 'status' in requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/50124?api_key={api_key}').json():
#     raise Exception("INVALID API KEY")