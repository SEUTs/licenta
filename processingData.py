def getGameEvolution(teamGoldPerMinuteDifferences):
    shortName = teamGoldPerMinuteDifferences
    limit = len(shortName)
    average = sum(shortName[:14]) / 14

    pathLength = 0
    if limit > 15:
        for i in range(1, 14):
            pathLength += abs(shortName[i+1] - shortName[i])
    
    earlySituation = 0

    if max([abs(x) for x in shortName[:14]]) < 2500:
        if pathLength / max(shortName[0:14]) > 2:
            earlyGame = "Chaotic neutral early game (min 0-14)"
        else:
            earlyGame = "Stable neutral early game (min 0-14)"
    else:
        if max(shortName[0:14]) > abs(min(shortName[0:14])):
            if pathLength / max(shortName[0:14]) > 2:
                earlyGame = "Chaotically won the early game (min 0-14)"
                earlySituation = 1
            else:
                earlyGame = "Solid win in the early game (min 0-14)"
                earlySituation = 2
        else:
            if pathLength / abs(min(shortName[0:14])) > 2:
                earlyGame = "Chaotically lost the early game (min 0-14)"
                earlySituation = -1
            else:
                earlyGame = "Solid loss in the early game (min 0-14)"
                earlySituation = -2
    


    pathLength = 0
    if limit > 15:
        for i in range(14, len(shortName) - 1):
            pathLength += abs(shortName[i+1] - shortName[i])

    if max([abs(x) for x in shortName[14:]]) < 2500:
        if pathLength / max(shortName[14:]) > 2:
            lateGame = f"Chaotic neutral late game (min 14-{len(shortName)})"
        else:
            lateGame = f"Stable neutral late game (min 14-{len(shortName)})"
    else:
        if max(shortName[14:]) > abs(min(shortName[14:])):
            if pathLength / max(shortName[14:]) > 2:
                lateGame = f"Chaotically won the late game (min 14-{len(shortName)})"
                lateSituation = 1
            else:
                lateGame = f"Solid win in the late game (min 14-{len(shortName)})"
                lateSituation = 2
        else:
            if pathLength / abs(min(shortName[14:])) > 2:
                lateGame = f"Chaotically lost the late game (min 14-{len(shortName)})"
                lateSituation = -1
            else:
                lateGame = f"Solid loss in the late game (min 14-{len(shortName)})"
                lateSituation = -2
    
    return (earlyGame, lateGame)