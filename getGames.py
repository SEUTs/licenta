import getMatchData
import licenta

for i in range(100):
    puuids = licenta.getSummonersWithRank(licenta.ranks[3], licenta.rankDistributions[3], licenta.rankQueue, page=i+1)
    for puuid in puuids:
        ids = licenta.GetMatchIds(puuid, 0, 100)
        for id in ids:
            getMatchData.saveMatchToFile(id)