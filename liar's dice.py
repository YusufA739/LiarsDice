import random,time,os,math


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
            cpugame(allPlayerHands,dieInHands,players,currentAction,nextAction,cpuMode)#give initial conditions to gameloop
        else:
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
    lastEject = "none"
    #when we start the game set this to true, so we can get new hands, it will reset to false anyway as actionTaken tells the code to gen new hands
    actionTaken = True #records any action taken against any other player, resets when new hands are generated, which will be due to flag being true
    names = takenames(players,cpuMode=False)  # Get player names (avoid use of magic number type of condition (pirate software XD))
    while validGame: #main game while loop

        #crown winner
        if players <= 1:
            validGame = False
            print("Game Over")
        else:
            currentAction,nextAction = selectPlayers(players,currentAction,nextAction,lastEject)#select new numbers for actions

            if actionTaken:#get new dice as last were revealed (irl version, may implement this later)
                allPlayerHands = generateHands(dieInHands)
                actionTaken = False
            else:
                actionTaken = False #reset flag for next round

            os.system('cls')  # Clear the console for a fresh view
            print("Player " + names[currentAction] + "'s turn")
            print("Your dice:",allPlayerHands[currentAction])
            dieCountFormatted = "\n"
            for carrier in range(players):
                dieCountFormatted = dieCountFormatted + "Player " + names[carrier] + ":" + str(dieInHands[carrier]) + "\n"
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
            print("Player " + names[nextAction] + "'s turn")
            print("Your dice:",allPlayerHands[nextAction])

            print("\nPlayer " + names[currentAction] + "'s bet:\n")
            print(dicegraphics(diceFace,minCount))

            bluffCall = input("Do you want to call:\n(b)bluff\n(s)spot on\n(c)continue, Player "+names[nextAction]+"?(b/s/<enter>):")
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
                    print("Valid bet from Player",names[currentAction],"so Player",names[nextAction],"loses a dice for an incorrect bluff call")
                    dieInHands[nextAction] = dieInHands[nextAction] - 1
                    if dieInHands[nextAction] == 0:
                        lastEject = "next"
                        allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,nextAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)
                else:
                    print("Invalid bet from Player",names[currentAction],"so Player",names[nextAction],"wins a dice for a correct bluff call")
                    dieInHands[currentAction] = dieInHands[currentAction] - 1
                    if dieInHands[currentAction] == 0:
                        lastEject = "current"
                        allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,currentAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)
                lastBet = 10
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
                    print("Bet from Player",names[currentAction],"was not exact, so Player",names[nextAction],"loses a dice for an incorrect spot on call")
                    dieInHands[nextAction] = dieInHands[nextAction] - 1
                    if dieInHands[nextAction] == 0:
                        lastEject = "next"
                        allPlayerHands,dieInHands,names = removePlayer(allPlayerHands,dieInHands,names,nextAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)
                else:
                    print("Bet from Player",names[currentAction],"was exact, so Player",names[nextAction],"wins a dice for a correct spot on call")
                    dieInHands[currentAction] = dieInHands[currentAction] - 1
                    if dieInHands[currentAction] == 0:
                        lastEject = "current"
                        allPlayerHands,dieInHands,names = removePlayer(allPlayerHands,dieInHands,names,currentAction)
                        players -= 1

                    print(allPlayerHands)
                    print(dieInHands)


            else:
                print("No action taken, Player "+names[nextAction]+" continues")
                time.sleep(1)
                print("Last Bet was "+str(currentBet)+". You must bet higher than this next round, by frequency or face or both")
                time.sleep(1)
                lastBet = currentBet
                lastFace = diceFace
                lastCount = minCount
                if (lastFace == 6 and lastCount == totalDiceCount):
                    print("Maximum bet reached, resetting bet...")
                    time.sleep(1)

        time.sleep(4)


def cpugame(allPlayerHands,dieInHands,players,currentAction,nextAction,cpuMode):
    validGame = True
    lastBet = 10
    lastFace = 0
    lastCount = 0
    actionTaken = True #records any action taken against any other player
    lastEject = "none"
    currentAction = random.randint(0,1)
    nextAction = 1 - currentAction
    names = takenames(players,cpuMode)
    while validGame: #main game while loop

        #if only 1 player remains... CROWN HIM WINNER!!!
        if players <= 1:
            validGame = False
            print("Game Over")
            print("Player " + names[0] + " wins!")
        else:#else, we should start by generating the action numbers
            temp = currentAction
            currentAction = nextAction
            nextAction = temp

            #regenerate hands if actions were taken (dice usually get shown in irl/gui modes)
            if actionTaken:
                allPlayerHands = generateHands(dieInHands)
                actionTaken = False
            else:
                pass#don't generate new hands

            os.system('cls')  # Clear the console for a fresh view
            #print(currentAction)debug due to old actioning code left in and causing bad behaviour (fixed)
            print("Player " + names[currentAction] + "'s turn")
            print("Your dice:",allPlayerHands[currentAction])
            dieCountFormatted = "\n"
            for carrier in range(players):
                dieCountFormatted = dieCountFormatted + "Player " + names[carrier] + ":" + str(dieInHands[carrier]) + "\n"
            print("\nPlayer Dice Count:"+dieCountFormatted)
            totalDiceCount = sum(dieInHands)

            while True:
                if currentAction == 0:  # Player's turn
                    try:
                        diceFace = int(input("Which face?"))
                        minCount = int(input("How much?"))
                        currentBet = int(str(diceFace) + str(minCount))

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
                            minCount = random.randint(minCount, minCount + random.randint(0,(round(totalDiceCount/2))))
                        elif minCount > 1:
                            #           -1  +  2 * (0 or 1) = 1 or -1
                            minCount += -1 + (2*round(random.random())) #avoid spot on so subtract or add 1
                        else:
                            pass

                    #bet limiter
                    currentBet = int(str(diceFace) + str(minCount))
                    newBet = 0
                    if currentBet <= lastBet:
                        if currentBet >= 40:
                            newBet = lastBet + random.randint(1,2)
                        else:
                            newBet = lastBet + 10 + random.randint(0,1)

                    break

            os.system('cls')
            if nextAction == 0:  # Player's turn
                print("Player " + names[nextAction] + "'s turn")
                print("Your dice:",allPlayerHands[nextAction])

                print("\nPlayer " + names[currentAction] + "'s bet:\n")
                print(dicegraphics(diceFace,minCount))

                bluffCall = input("Do you want to call:\n(b)bluff\n(s)spot on\n(c)continue, Player "+names[nextAction]+"?(b/s/<enter>):")
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
                        print("Valid bet from Player",names[currentAction],"so Player",names[nextAction],"loses a dice for an incorrect bluff call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                    else:
                        print("Invalid bet from Player",names[currentAction],"so Player",names[nextAction],"wins a dice for a correct bluff call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                    lastBet = 10
                elif bluffCall.lower() == "s":
                    print("Player",names[nextAction],"calls spot on, on Player",names[currentAction])
                    time.sleep(1)
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
                        print("Bet from Player",names[currentAction],"was not exact, so Player",names[nextAction],"loses a dice for an incorrect spot on call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                    else:
                        print("Bet from Player",names[currentAction],"was exact, so Player",names[nextAction],"wins a dice for a correct spot on call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)


                else:
                    print("No action taken, Player ",names[nextAction]," continues")
                    time.sleep(1)
                    print("Last Bet was "+str(currentBet)+". You must bet higher than this next round, by frequency or face or both")
                    lastBet = currentBet
                    lastFace = diceFace
                    lastCount = minCount
                    if (lastFace == 6 and lastCount == totalDiceCount):
                        print("Maximum bet reached, resetting bet...")
                        time.sleep(1)
            else:#CPU's turn
                #check if player even has enough dice for bet
                #cpuCount = minCount - sum(1 for die in allPlayerHands[nextAction] for dice in die if dice == diceFace)
                cpuCount = minCount - allPlayerHands[nextAction].count(diceFace)
                if cpuCount <= 1:#player got min number correct or player has once dice of that face as well as cpu having all of that face (can code in a 50/50 bluff when cpuCount == 1)
                    bluffCall = "n"
                elif cpuCount/len(allPlayerHands[currentAction]) >= 0.5 and cpuCount > 1: #if player has >=60% of the dice, call bluff
                    bluffCall = "b"
                else:
                    bluffCall = "n"
                    
                    
                if bluffCall.lower() == "y" or bluffCall.lower() == "b":
                    print("Player",names[nextAction]," calls bluff on Player ",names[currentAction])
                    time.sleep(1)
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
                        print("Valid bet from Player",names[currentAction],"so Player",names[nextAction],"loses a dice for an incorrect bluff call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                    else:
                        print("Invalid bet from Player",names[currentAction],"so Player",names[nextAction],"wins a dice for a correct bluff call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                    lastBet = 10
                elif bluffCall.lower() == "s":
                    print("Player",names[nextAction],"calls spot on, on Player",names[currentAction])
                    time.sleep(1)
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
                        print("Bet from Player",names[currentAction],"was not exact, so Player",names[nextAction],"loses a dice for an incorrect spot on call")
                        dieInHands[nextAction] = dieInHands[nextAction] - 1
                        if dieInHands[nextAction] == 0:
                            lastEject = "next"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,nextAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)
                    else:
                        print("Bet from Player",names[currentAction],"was exact, so Player",names[nextAction],"wins a dice for a correct spot on call")
                        dieInHands[currentAction] = dieInHands[currentAction] - 1
                        if dieInHands[currentAction] == 0:
                            lastEject = "current"
                            allPlayerHands, dieInHands, names = removePlayer(allPlayerHands, dieInHands, names,currentAction)
                            players -= 1

                        print(allPlayerHands)
                        print(dieInHands)


                else:
                    print("No action taken, Player ",names[nextAction]," continues")
                    time.sleep(1)
                    print("Last Bet was "+str(currentBet)+". You must bet higher than this next round, by frequency or face or both")
                    lastBet = currentBet
                    lastFace = diceFace
                    lastCount = minCount
                    if (lastFace == 6 and lastCount == totalDiceCount):
                        print("Maximum bet reached, resetting bet...")
            time.sleep(4)


def generateHands(dieinhands):#playercount not needed as len(dieInHands) represents info good enough
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

def removePlayer(hands,diecounts,givennames,index):
    if len(hands) != len(diecounts):#user has given incorrect lengths of lists
        raise ValueError("Hands and die counts must be of the same length.")
    if index > len(hands):
        raise IndexError("Index out of range (too large i). Cannot remove player at index " + str(index) + ".")
    else:
        new_list1=[]
        new_list2=[]
        new_list3=[]
        for carrier in range(len(hands)):
            if carrier == index:
                pass
            else:
                new_list1.append(hands[carrier])
                new_list2.append(diecounts[carrier])
                new_list3.append(givennames[carrier])
        return new_list1,new_list2, new_list3

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
        graphics = ("""Invalid number for dice graphics.
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

def takenames(no_of_players,cpuMode):
    localnames = []
    if not cpuMode:
        for i in range(no_of_players):
            while True:
                name = input("Enter name for Player " + str(i) + ": ")
                if name.strip() == "":
                    print("Name cannot be empty. Please enter a valid name.")
                elif name in localnames:
                    print("Name already taken. Please choose a different name.")
                else:
                    localnames.append(name)
                    break
    else:
        player1name = ""
        cpuName = "T-800"
        while player1name.strip() == "" or player1name in localnames or player1name.lower() == cpuName:
            player1name = input("Enter name: ")
        localnames.append(player1name)
        localnames.append(cpuName)
        
    return localnames

def selectPlayers(players,current,next,lasteject):
    maxIndex = players
    if lasteject == "current":
        if current <= maxIndex-1:#has to be second to last or less, so next does not get assigned out of bounds
            pass
        elif current == maxIndex:
            next = 0
        elif current > maxIndex:
            current = 0
            next = current + 1
        else:
            print("selectPlayers('current',...) failed cond check")
    elif lasteject == "next":
        if next >= maxIndex:
            current = maxIndex
            next = 0
        elif next <= maxIndex-1:
            current += 1
            next = current + 1
        else:
            print("selectPlayers('next',...) failed cond check")
    elif lasteject == "none":
        if current >= maxIndex:#should never execute
            current = 0
            next = current + 1
        elif current == maxIndex-1:
            current = maxIndex
            next = 0
        elif current < maxIndex-1:
            current = current + 1
            next = current + 1
        else:
            print("selectPlayers('none',...) failed cond check")

    return current,next



setupReturn = 0
while setupReturn == 0:
    setupReturn = setup()