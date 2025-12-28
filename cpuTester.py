import random
from liarsDice import cpuBet
def testBetting():
    allPlayerHands = [[],[]]
    for carrier in range(2):
        for carrier2 in range(5):
            allPlayerHands[carrier].append(random.randint(1,6))
    lastFace, lastCount = 3, 3
    lastBet = int(str(lastFace) + str(lastCount))
    diceFace, minCount = cpuBet(allPlayerHands, 1, 3, 4, 0, 0, 1, 3, 3)
    currentBet = int(str(diceFace) + str(minCount))
    assert (diceFace >= 0)
    assert (minCount > 0)
    assert (currentBet > lastBet)

for carrier in range(100):#repeat n times and see how stable the cpuBetting is
    testBetting()