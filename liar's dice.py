import random,time,os


def setup():
    dieInHands = []
    allPlayerHands = []
    cpuMode = False

    os.system('cls')
    try:
        players = int(input("How many players?"))
        if players < 1:
            print("Defaulting to P v CPU mode")
            players = 2
            cpuMode = True
        elif players == 1:
            players = 2
            cpuMode = True
        else:
            pass

        for placeholder in range(players):
            dieInHands.append(5)

        tempIndex = 0
        for dieCount in dieInHands:
            allPlayerHands.append([0])
            blankArray = []
            for placeholder in range(dieCount):
                blankArray.append(0)
            allPlayerHands[tempIndex] = blankArray
            tempIndex = tempIndex + 1

        currentAction = 0
        nextAction = currentAction + 1

        if cpuMode:
            print("CPU Mode enabled. Player 0 is you, Player 1 is the CPU.")
            

        game(allPlayerHands,dieInHands,players,currentAction,nextAction)#give initial conditions to gameloop
        playAgain = input("Play again? (y/n)")
        if playAgain == "y" or playAgain == "yes":
            return 0
        else:
            return 1
    except ValueError:
        return 0


def game(allPlayerHands,dieInHands,players,currentAction,nextAction):
    validGame = True
    lastBet = 10
    lastFace = 0
    lastCount = 0
    actionTaken = False #records any action taken against any other player 
    while validGame: #main game while loop
        for i in range(len(dieInHands)):#check all players have more than 0 dice in hand
            if (dieInHands[i]) > 0:
                pass
            elif (dieInHands[i]) == 0:#precheck to remove players and prevent next action (bluff call) being
                allPlayerHands,dieInHands = removePlayer(allPlayerHands,dieInHands,i)
                players -= 1
        if players <= 1:
            validGame = False
            print("Game Over")
        else:
            if currentAction >= players:#loop it back around
                currentAction = players - 1
            if nextAction >= players:#loop it back around
                nextAction = 0

            if not actionTaken:
                allPlayerHands = generateHands(dieInHands,players)
            else:
                actionTaken = False #reset flag for next round

            os.system('cls')  # Clear the console for a fresh view
            print("Player " + str(currentAction) + "'s turn")
            print("Your dice:",allPlayerHands[currentAction])
            dieCountFormatted = "\n"
            for carrier in range(players):
                dieCountFormatted = dieCountFormatted + "Player " + str(carrier) + ":" + str(dieInHands[carrier]) + "\n"
            print("\nPlayer Dice Count:"+dieCountFormatted)

            while True:
                try:
                    diceFace = int(input("Which face?"))
                    minCount = int(input("How much?"))
                    currentBet = int(str(diceFace) + str(minCount))
                    
                    totalDiceCount = sum(dieInHands)
                    if currentBet > lastBet and minCount <= totalDiceCount and minCount >= 1 and diceFace <= 6 and diceFace >= 1:
                        lastBet = currentBet #not needed, but is valid anyway
                        break
                    else:
                        if not currentBet > lastBet:
                            print("Bet is less than last bet.\nYour bet:",currentBet,"    Last bet:",lastBet)
                        time.sleep(2)
                except ValueError:
                    print("Invalid input. Integers only for face and count.")

            os.system('cls')
            print("Player " + str(nextAction) + "'s turn")
            print("Your dice:",allPlayerHands[nextAction])

            print("\nPlayer " + str(currentAction) + "'s bet:\n")
            print(dicegraphics(diceFace,minCount))

            bluffCall = input("Do you want to call:\n(b)bluff\n(s)spot on\n(c)continue, Player "+str(nextAction)+"?(b/s/<enter>):")
            if bluffCall.lower() == "y" or bluffCall.lower() == "b":
                
                actionTaken = True

                actualcount = 0
                validBet = False
                for hand in allPlayerHands:
                    for dice in hand:
                        if dice == diceFace:
                            actualcount = actualcount + 1
                if actualcount >= minCount:
                    validBet = True

                if validBet:
                    print("Valid bet from Player",currentAction,"so Player",nextAction,"loses a dice for an incorrect bluff call")
                    dieInHands[nextAction] = dieInHands[nextAction] - 1
                    print(allPlayerHands)
                    print(dieInHands)
                else:
                    print("Invalid bet from Player",currentAction,"so Player",nextAction,"wins a dice for a correct bluff call")
                    dieInHands[currentAction] = dieInHands[currentAction] - 1
                    print(allPlayerHands)
                    print(dieInHands)
                lastBet = 11
            elif bluffCall.lower() == "s":
                
                actionTaken = True

                actualcount = 0
                validBet = False
                for hand in allPlayerHands:
                    for dice in hand:
                        if dice == diceFace:
                            actualcount = actualcount + 1
                if actualcount == minCount:
                    validBet = False

                if validBet:
                    print("Bet from Player",currentAction,"was not exact, so Player",nextAction,"loses a dice for an incorrect spot on call")
                    dieInHands[nextAction] = dieInHands[nextAction] - 1
                    print(allPlayerHands)
                    print(dieInHands)
                else:
                    print("Bet from Player",currentAction,"was exact, so Player",nextAction,"wins a dice for a correct spot on call")
                    dieInHands[currentAction] = dieInHands[currentAction] - 1
                    print(allPlayerHands)
                    print(dieInHands)


            else:
                print("No action taken, Player "+str(nextAction)+" continues")
                time.sleep(1)
                print("Last Bet"+str(currentBet)+". You must bet higher than this next round, by frequency or face or both")
                time.sleep(1)
                lastBet = currentBet
                lastFace = diceFace
                lastCount = minCount
                if (lastFace == 6 and lastCount == totalDiceCount):
                    print("Maximum bet reached, resetting bet...")
                    time.sleep(1)

            currentAction = nextAction
            nextAction = currentAction + 1


def cpugame(allPlayerHands,dieInHands,players,currentAction,nextAction):
    validGame = True
    lastBet = 10
    lastFace = 0
    lastCount = 0
    actionTaken = False #records any action taken against any other player 
    while validGame: #main game while loop
        for i in range(len(dieInHands)):#check all players have more than 0 dice in hand
            if (dieInHands[i]) > 0:
                pass
            elif (dieInHands[i]) == 0:#precheck to remove players and prevent next action (bluff call) being
                allPlayerHands,dieInHands = removePlayer(allPlayerHands,dieInHands,i)
                players -= 1
        if players <= 1:
            validGame = False
            print("Game Over")
        else:
            if currentAction >= players:#loop it back around
                currentAction = players - 1
            if nextAction >= players:#loop it back around
                nextAction = 0

            if not actionTaken:
                allPlayerHands = generateHands(dieInHands,players)
            else:
                actionTaken = False #reset flag for next round

            os.system('cls')  # Clear the console for a fresh view
            print("Player " + str(currentAction) + "'s turn")
            print("Your dice:",allPlayerHands[currentAction])
            dieCountFormatted = "\n"
            for carrier in range(players):
                dieCountFormatted = dieCountFormatted + "Player " + str(carrier) + ":" + str(dieInHands[carrier]) + "\n"
            print("\nPlayer Dice Count:"+dieCountFormatted)

            while True:
                if currentAction == 0:  # Player's turn
                    try:
                        diceFace = int(input("Which face?"))
                        minCount = int(input("How much?"))
                        currentBet = int(str(diceFace) + str(minCount))
                        
                        totalDiceCount = sum(dieInHands)
                        if currentBet > lastBet and minCount <= totalDiceCount and minCount >= 1 and diceFace <= 6 and diceFace >= 1:
                            lastBet = currentBet #not needed, but is valid anyway
                            break
                        else:
                            if not currentBet > lastBet:
                                print("Bet is less than last bet.\nYour bet:",currentBet,"    Last bet:",lastBet)
                            time.sleep(2)
                    except ValueError:
                        print("Invalid input. Integers only for face and count.")
                else:#cpu's turn
                    diceFace = random.randint(1, 6)
                    minCount = 0
                    for i in range(len(allPlayerHands[currentAction])):
                        if allPlayerHands[currentAction][i] == diceFace:
                            minCount += 1
                    
                    if minCount == 0:
                        minCount = 1#bluff it anyway, don't bother playing it safe and rerolling the diceFace we want
                    else:
                        if dieInHands[1] > dieInHands[0]:#if cpu has more dice than player, we add some extra dice to be more risky (if that prob plays out), otherwise play it safe
                            minCount = random.randint(minCount, minCount + random.randint(0, totalDiceCount - totalDiceCount // 2))
                        else:
                            #           -1  +  2 * (0 or 1) = 1 or -1
                            minCount += -1 + (2*round(random.random())) #avoid spot on so subtract or add 1

            os.system('cls')
            if currentAction == 0:  # Player's turn
                print("Player " + str(nextAction) + "'s turn")
                print("Your dice:",allPlayerHands[nextAction])

                print("\nPlayer " + str(currentAction) + "'s bet:\n")
                print(dicegraphics(diceFace,minCount))

                bluffCall = input("Do you want to call:\n(b)bluff\n(s)spot on\n(c)continue, Player "+str(nextAction)+"?(b/s/<enter>):")
                if bluffCall.lower() == "y" or bluffCall.lower() == "b":
                    
                    actionTaken = True

                    actualcount = 0
                    validBet = False
                    for hand in allPlayerHands:
                        for dice in hand:
                            if dice == diceFace:
                                actualcount = actualcount + 1
                    if actualcount >= minCount:
                        validBet = True

                    if validBet:
                        print("Valid bet from Player",currentAction,"so Player",nextAction,"loses a dice for an incorrect bluff call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        print(allPlayerHands)
                        print(dieInHands)
                    else:
                        print("Invalid bet from Player",currentAction,"so Player",nextAction,"wins a dice for a correct bluff call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        print(allPlayerHands)
                        print(dieInHands)
                    lastBet = 11
                elif bluffCall.lower() == "s":
                    
                    actionTaken = True

                    actualcount = 0
                    validBet = False
                    for hand in allPlayerHands:
                        for dice in hand:
                            if dice == diceFace:
                                actualcount = actualcount + 1
                    if actualcount == minCount:
                        validBet = False

                    if validBet:
                        print("Bet from Player",currentAction,"was not exact, so Player",nextAction,"loses a dice for an incorrect spot on call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        print(allPlayerHands)
                        print(dieInHands)
                    else:
                        print("Bet from Player",currentAction,"was exact, so Player",nextAction,"wins a dice for a correct spot on call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        print(allPlayerHands)
                        print(dieInHands)


                else:
                    print("No action taken, Player "+str(nextAction)+" continues")
                    time.sleep(1)
                    print("Last Bet"+str(currentBet)+". You must bet higher than this next round, by frequency or face or both")
                    time.sleep(1)
                    lastBet = currentBet
                    lastFace = diceFace
                    lastCount = minCount
                    if (lastFace == 6 and lastCount == totalDiceCount):
                        print("Maximum bet reached, resetting bet...")
                        time.sleep(1)
            else:#CPU's turn
                pass

            currentAction = nextAction
            nextAction = currentAction + 1


def generateHands(dieinhands,playercount):
    player = 0
    allplayerhands = []
    tempArray = []
    for diecount in dieinhands:
        for dice in range(diecount):
            tempArray.append(0)
        allplayerhands.append(tempArray)
        tempArray = []
        for dice in range(diecount):
            allplayerhands[player][dice] = random.randint(1,6)
        player = player + 1
    return allplayerhands

def removePlayer(hands,diecounts,index):
    if len(hands) != len(diecounts):
        return hands,diecounts
    if index > len(hands):
        return hands,diecounts
    else:
        new_list1=[]
        new_list2=[]
        for carrier in range(len(hands)):
            if carrier == index:
                pass
            else:
                new_list1.append(hands[carrier])
                new_list2.append(diecounts[carrier])
        return new_list1,new_list2

def dicegraphics(number,frequency):
    if number != int:
        try:
            number = int(number)
        except ValueError:
            return "Invalid input for dice graphics. Please enter an integer between 1 and 6."
            
    graphics = ""
    if number == 1:
        graphics += (" ---------") + "\n"
        graphics += ("|         |") + "\n"
        graphics += ("|    *    |   x     " + str(frequency)) + "\n"
        graphics += ("|         |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 2:
        graphics += (" ---------") + "\n"
        graphics += ("| *       |") + "\n"
        graphics += ("|         |   x     " + str(frequency)) + "\n"
        graphics += ("|       * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 3:
        graphics += (" ---------") + "\n"
        graphics += ("| *       |") + "\n"
        graphics += ("|    *    |   x     " + str(frequency)) + "\n"
        graphics += ("|       * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 4:
        graphics += (" ---------") + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += ("|         |   x     " + str(frequency)) + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 5:
        graphics += (" ---------") + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += ("|    *    |   x     " + str(frequency)) + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += (" ---------") + "\n"
    elif number == 6:
        graphics += (" ---------") + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += ("| *     * |   x     " + str(frequency)) + "\n"
        graphics += ("| *     * |") + "\n"
        graphics += (" ---------") + "\n"
    else:
        graphics("""Invalid number for dice graphics.
              Dice graphics will not perform error handling.
              You must perform error handling beforehand, 
              by checking if user submitted a number within 1-6 dice range.""")
    return graphics

def guessDice(count, side, ownDice, players, diceRemaining, playerNum):
    dice = []

    diceRemaining[playerNum] = 0

    for carrier in range(players):
        diceGen = []
        for carrier2 in range(diceRemaining[carrier]):
            diceGen.append(random.randint(1, 6))
        if len(diceGen) > 0:    
            dice.append(diceGen)

    dice.append(ownDice)

    for hand in dice:
        for d in hand:
            if d == side:
                count -= 1

    if count <= 0:
        return True
    else:
        return False

def CPU():
    pass


setupReturn = 0
while setupReturn == 0:
    setupReturn = setup()