from fightsWithVariousShips import *
from displayTable import *
from time import time


def approximateTime(NBships, NBfights):
    t1 = time()
    for i in range(3):
        ship = createRandomShip(400)
        ship2 = createRandomShip(400)
        fightsWithFileName(1, ship, ship2)
        deleteShip(ship)
        deleteShip(ship2)
    t2 = time()
    timeF = (t2 - t1)/3
    nbcore = mp.cpu_count()
    nb = NBfights * ((NBships-1)*(NBships/2))
    print('')
    print("============  Estimation of tournament's time  =============")
    print('For '+str(NBships)+' ships with '+str(NBfights)+' rounds')
    print('Number of core : '+str(nbcore))
    print('Number of fights : '+str(nb))
    print('Time for one fight : '+str(timeF))
    print('Total time : '+str(nb*timeF/(60*nbcore))+'mn')
    print('')


def tournament(listShips, nbFights):
    listShip = listShips[:]
    # t1 = time()
    copylistShip = listShip[:]

    victories = {}
    for s in listShips:
        victories[s] = 0

    # nb = nbFights * ((len(listShip)-1)*(len(listShip)/2))

    if printTournament:
        tableResults = [[0]*len(listShip) for _ in range(len(listShip))]
        numbers = {}
        for i in range(len(listShip)):
            numbers[listShip[i]] = i

    for indexT in range(len(listShip)):
        ship1 = listShip[0]
        listShip = listShip[1:]
        for ship2 in listShip:
            lRes = fightsWithFileName(nbFights, ship1, ship2)
            # print(l)
            cpt1 = lRes.count("Ship 1 won")
            cpt2 = len(lRes)-cpt1
            tot = cpt1 + cpt2

            if cpt1 == 0:
                victories[ship2] += 1
            elif cpt2 == 0:
                victories[ship1] += 1
            else:
                if cpt1/tot > 0.50:
                    victories[ship1] += 1
                elif cpt2/tot > 0.50:
                    victories[ship2] += 1

            if printTournament:

                nbship1 = numbers[ship1]
                nbship2 = numbers[ship2]
                tableResults[nbship1][nbship2] += cpt1
                tableResults[nbship2][nbship1] += cpt2

    if printTournament:
        sendTable(copylistShip, tableResults, nbFights)

    # t2 = time()
    # print('Total time : '+str((t2-t1)/60)+'mn')
    # print('Number of fights : '+str(nb))
    # print('Time for one fight : '+str((t2-t1)/nb))

    print(victories)

    return victories