import random
import time

# words that will be used in text as game commentary
NUMBERWORDS = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three twenty-four twenty-five'.split()
NUMBERPLURALS = 'q ones twos threes fours fives sixes'.split()
# different names for the opponents
names = 'Jack William Elizabeth Hector Davy Blackbeard Kraken Salazar Calypso Gibbs Norrington Angelica Philip Groves Pintel Ragetti'.split()

def pause():
    time.sleep(1)

# Start of the game,defines number of players
def startGame():
    bad = True
    while bad:
        print("\nHow many players?")
        p = input()
        if p.isdigit():
            p = int(p)    
            if p < 2 or p > 5:
                print("Please choose a number of players from 2 to 5.")
            else:
                bad = False
    return p

# initializes the computer as the opponent and gives it a random name
def initNPC(numCPU):
    cpuP = []
    for x in range(numCPU):
        n = names[random.randint(0,len(names)-1)]
        names.remove(n)
        cpuP.append([[0,0,0,0,0],5,n,False])
    return cpuP

# rolls the dice
def rollDice(playerInfo):
    # uses an array of 4 slots for each player, each slot for each dice
    playerInfo[0] = [0,0,0,0,0]
    # uses random module for the random outcome of the dice rolling
    for x in range(playerInfo[1]):
        playerInfo[0][x] = random.randint(1,6)
    # uses a sorting method for a more clear display of the dices
    playerInfo[0].sort()
    return playerInfo

def validBet (oldBet, newBet):
    if oldBet[0] > newBet[0] or (oldBet[0] == newBet[0] and oldBet[1] >= newBet[1]) or newBet[0]>24 or newBet[1]>6: 
        return False
    else:
        return True

def bet(who,p,oldBet):
    newbet = [0,0]
    if p[who][3]:
        wrong = True
        while wrong:
            print('What you like to bet? [Number of dice] [Value of dice]')
            newbet = input()
            #print(newbet)
            newbet = newbet.split()
            if len(newbet) > 1 and newbet[0].isdigit() and newbet[1].isdigit():
                newbet = [int(newbet[0]),int(newbet[1])]
                if validBet(oldBet,newbet):
                    wrong = False
                
    else:
        bestValue = oldBet[1]
        bestOdds = 0
        for x in range(1,7):
            odds = calcOdds(who,p,x)
            if x <= oldBet[1]:
                odds -= 1
            if odds > bestOdds:
                bestValue = x
                bestOdds = odds
        if bestValue <= oldBet[1]:
            newbet[0] = oldBet[0]+1
        else:
            newbet[0] = oldBet[0]
        newbet[1] = bestValue

    print(p[who][2] + ' bets that there are ' +NUMBERWORDS[newbet[0]] + ' ' + NUMBERPLURALS[newbet[1]] + ' on the table.\n')
    pause()
    pause()
    return newbet
                    
        
def calcOdds(who,p,value):
    numOfDice = 0
    for x in range(maxPlayers):
        numOfDice += p[x][1]
    numOfDice -= p[who][1]
    return round(numOfDice/6)+p[who][0].count(value)

def humanChoice(prevPlayer):
    print('Would you like to [b]et, call ' + prevPlayer + ' a [l]iar, or declare the last bet [s]pot on?')
    fake = True
    while fake:
        d = input()
        if d == 'b':
            return 0
        if d == 'l':
            return 1
        if d == 's':
            return 2
        print('Invalid input. Please enter the letter b, l, or s.')

def cpuChoice(who,p,oldBet):
    odds = calcOdds(who,p,oldBet[1])
    if oldBet[0] == odds:
        if random.randint(0,1) == 0:
            return 2
        else:
            return 0
    if oldBet[0] > odds:
        return 1
    else:
        return 0

def countDice(p,value):
    total = 0
    for x in range(maxPlayers):
        d = p[x][0].count(value)
        total = d + total
        print(p[x][2] + ' has ' + NUMBERWORDS[d] + ' ' + NUMBERPLURALS[value] + '.', end=' ')
        for y in range(5):
            if p[x][0][y] != 0:
                print('[' + str(p[x][0][y]) + ']', end=' ')
        print()
        pause()
    pause()
    print('There are a total of ' + NUMBERWORDS[total] + ' ' + NUMBERPLURALS[value] + ' on the table.\n')
    pause()
    return total

def bluff(who,p,oldBet):
    print(p[who][2] + ' thinks ' + p[(who-1)%maxPlayers][2] + ' is full of it.\n')
    if countDice(p,oldBet[1]) >= oldBet[0]:
        p[who][1] -= 1
        print('Bad call. ' + p[who][2] + ' loses a die, they now have ' + NUMBERWORDS[p[who][1]] + ' dice.')
    else:
        p[(who-1)%maxPlayers][1] -= 1
        print('Great call, '+ p[who][2] + '! '+ p[(who-1)%maxPlayers][2] + ' loses a die. They now have only ' + NUMBERWORDS[p[(who-1)%maxPlayers][1]] + ' dice.\n')
    return p

def spotOn(who,p,oldBet):
    print(p[who][2] + ' thinks ' + p[(who-1)%maxPlayers][2] +  ' is spot on.\n')
    if countDice(p,oldBet[1]) == oldBet[0]:
        print('Great call, ' + p[who][2] + '! Everyone else loses a die.\n')
        for x in range(maxPlayers):
            if x != who:
                p[x][1] -= 1
                print(p[x][2] + ' now has ' + NUMBERWORDS[p[x][1]] + ' dice.')
    else:
        p[who][1] -= 1
        print('Bad call. ' + p[who][2] + ' loses a die, they now have ' + NUMBERWORDS[p[who][1]] + ' dice.\n')
    pause()
    pause()
    return p

def removePlayers(p):
    mP = maxPlayers
    dead = []
    for x in range(maxPlayers):
        if p[x][1] == 0:
            mP -= 1
            print(p[x][2] + ' is out of the game.\n')
            pause()
            dead.append(x)
            
    for x in range(len(dead)):
        p.pop(dead[x])
    pause()
    return [p, mP]
    
        
print('What is your name?')
temp = input()
maxPlayers = startGame()
players = initNPC(maxPlayers-1)
players.append([[0,0,0,0,0],5,temp,True])

    
gameContinues = True
goesNext = random.randint(0,maxPlayers-1)

while gameContinues:   
    for x in range(maxPlayers):
        players[x] = rollDice(players[x])
        
    roundContinues = True
    currentBet = [0,6]
    if players[goesNext][3]:
        print('\nYour hand: ')
        t = 0
        for y in range(5):
            if players[goesNext][0][y] != 0:
                print('[' + str(players[goesNext][0][y]) + ']', end=' ')
            if y < maxPlayers:
                t += players[y][1]
        print('\nThere are ' + str(t-players[goesNext][1]) + ' other dice on the table.\n')
    print(players[goesNext][2] + ' starts. Please place the first bet.\n')
    currentBet = bet(goesNext,players,currentBet)
    while roundContinues:
        goesNext = (goesNext+1)%(maxPlayers)
        if players[goesNext][3]:
            print("It's your turn. Your hand: ", end="")
            t = 0
            for y in range(5):
                if players[goesNext][0][y] != 0:
                    print('[' + str(players[goesNext][0][y]) + ']', end=' ')
                if y < maxPlayers:
                    t += players[y][1]
            print('\nThere are ' + str(t-players[goesNext][1]) + ' other dice on the table.')
            choice = humanChoice(players[(goesNext-1)%(maxPlayers)][2])
        else:
            choice = cpuChoice(goesNext,players,currentBet)
        if choice == 0:
            currentBet = bet(goesNext,players,currentBet)
        elif choice == 1:
            players = bluff(goesNext,players,currentBet)
            roundContinues = False
        elif choice == 2:
            players = spotOn(goesNext,players,currentBet)
            roundContinues = False
    temp = removePlayers(players)
    players = temp[0]
    if maxPlayers != temp[1]:
        maxPlayers = temp[1]
        goesNext = (goesNext-1)%maxPlayers
    temp = []


    if maxPlayers == 1:
        gameContinues = False
        print('\nCongratulations! ' + players[goesNext][2] + ' is the winner.')