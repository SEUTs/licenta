import getMastery
import licenta

for i in range(100):
    puuids = licenta.getSummonersWithRank(licenta.ranks[3], licenta.rankDistributions[3], licenta.rankQueue, page=i+1)
    for puuid in puuids:
        getMastery.getMasteries(puuid, "eun")