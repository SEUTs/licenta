
if 'status' in requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/50124?api_key={api_key}').json():
    raise Exception("INVALID API KEY")