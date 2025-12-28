import random
from liarsDice import cpuBet
def generateHandsForTests():
    allPlayerHands = [[], []]
    for carrier in range(2):
        for carrier2 in range(5):
            allPlayerHands[carrier].append(random.randint(1, 6))
    return allPlayerHands

def testBetting(allPlayerHands,lastFace,lastCount):
    lastBet = int(str(lastFace) + str(lastCount))
    diceFace, minCount = cpuBet(allPlayerHands, 1, lastFace, lastCount, 0, 0, 1, 3, 3)
    currentBet = int(str(diceFace) + str(minCount))
    assert (diceFace >= 0)
    assert (minCount > 0)
    assert (currentBet > lastBet)
    return currentBet

face = 3
count = 3
lastBet = int(str(face) + str(count))
print("Last Bet:", lastBet)
for carrier in range(10):
    print("Hand:",carrier+1)
    currentHands = generateHandsForTests()
    print("Current Hands:",currentHands)
    for carrier2 in range(10):#repeat n times and see how stable the cpuBetting is
        print("Iteration:",carrier2+1)
        cBet = testBetting(currentHands,face,count)
        print("Current Bet:",cBet)