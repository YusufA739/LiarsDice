import random
from ..liarsDice import cpuBet
def testBetting():
    allPlayerHands = [[],[]]
    for carrier in range(2):
        for carrier2 in range(5):
            allPlayerHands[carrier].append(random.randint(1,6))
    diceFace, minCount = cpuBet(allPlayerHands, 1, 0, 3, 0, 0, 1, 3, 3)
    assert (diceFace >= 0)
    assert (minCount < 0)
testBetting()