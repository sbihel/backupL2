from expertSystem import *


def multipleOptimization(maxCost, nbCombats, sizeFirstPopulation, nbInitGeneticAlgo=1):
    """
    Takes a lot of time to do multiple techniques to determine the best
    """
    nbChampions = sizeFirstPopulation//3
    if nbChampions < 2:
        nbChampions = 2
    hallOfFame, hallOfShame, oldChampions = [], [], []
    for _ in range(nbInitGeneticAlgo):
        gAlgo = autoStopGeneticAlgorithm(sizeFirstPopulation, maxCost, nbCombats, nbChampions=nbChampions)
        hallOfFame += gAlgo[0]
        hallOfShame += gAlgo[1]
        oldChampions += [gAlgo[2]]

    allFeaturesF = getBestFeatures(buildLCMInputFile(hallOfFame+hallOfShame))
    # bestFeaturesF = getBestFeatures(buildLCMInputFile(hallOfFame))
    # worstFeaturesF = getBestFeatures(buildLCMInputFile(hallOfShame))
    newShips = hallOfFame[:]

    newShips += [shipV for shipV in expertSystem(allFeaturesF, hallOfFame, hallOfShame, maxCost) if seemsNotBad(shipV)]
    # newShips += oldExpertSystem(bestFeaturesF, worstFeaturesF, maxCost, len(hallOfFame), len(hallOfShame), oldChampions,
    #                          nbChampions)
    # shuffle(newShips)
    # nbFinalGA = 2
    # nbNewShips = len(newShips)
    # newShipsFinal = []
    # for nbGA in range(nbFinalGA):
    #     index1 = nbGA * (nbNewShips//nbFinalGA)
    #     index2 = (nbGA + 1) * (nbNewShips // nbFinalGA)
    #     if nbGA == nbFinalGA - 1:
    #         index2 = nbNewShips
    #     newShipsFinal += autoStopGeneticAlgorithm(len(newShips[index1:index2]), maxCost, nbCombats,
    #                                               initChampions=newShips[index1:index2])[0]
    # return autoStopGeneticAlgorithm(len(newShips), maxCost, nbCombats, initChampions=newShips)[0]

    # subjectiveShips = [createSubjectiveGoodShip(maxCost) for _ in range(5)]
    # newShips += subjectiveShips[:]

    finalTournament = tournament(newShips, nbCombats)
    bestIndividual = newShips[0]
    for k in finalTournament:
        if finalTournament[k] > finalTournament[bestIndividual]:
            bestIndividual = k
    # if bestIndividual in subjectiveShips:
    #     print('Looks like this ship is from the homemade expert system...')
    return bestIndividual


def oldExpertSystem(bestFeaturesF, worstFeaturesF, maxCost, nbChampions, nbNoobs, oldChampions, nbChampionsPerTurn):
    uniqueBestFeatures = bestFeaturesNotInWorstFeatures(bestFeaturesF, worstFeaturesF, nbChampions, nbNoobs)
    # dominantFeatures = bestFeaturesFromGrowthRate(oldChampions, nbChampionsPerTurn)

    newShips = []

    # ships = {'kestrel': ['typeA', 'typeB', 'typeC'],
    #          'engiCruiser': ['typeA']}

    with open(uniqueBestFeatures) as bF:
        for line in bF:
            for s in shipsSupported:
                for t in shipsSupported[s]:
                    nameN = s
                    typeN = t
                    systemsUpgrades, weaponsP, dronesP, energyP = addingToShipFromLCMLine(line, nameN, typeN)
                    newShips += [createRandomShip(maxCost,
                                                  nameShip=nameN, typeShip=typeN,
                                                  systemsUpgradesWanted=systemsUpgrades,
                                                  weaponsWanted=weaponsP,
                                                  dronesWanted=dronesP,
                                                  energyWanted=energyP)]

    return newShips


def expertSystem(allFeatures, goodShips, badShips, maxCost):
    uniqueBestFeatures = bestFeaturesFromGrowthRate(allFeatures, goodShips, badShips)

    newShips = []
    with open(uniqueBestFeatures) as bF:
        for line in bF:
            for s in shipsSupported:
                for t in shipsSupported[s]:
                    nameN = s
                    typeN = t
                    systemsUpgrades, weaponsP, dronesP, energyP = addingToShipFromLCMLine(line, nameN, typeN)
                    newShips += [createRandomShip(maxCost,
                                                  nameShip=nameN, typeShip=typeN,
                                                  systemsUpgradesWanted=systemsUpgrades,
                                                  weaponsWanted=weaponsP,
                                                  dronesWanted=dronesP,
                                                  energyWanted=energyP)]
    return newShips


def createSubjectiveGoodShip(maxCost):
    newShip = createRandomShip(maxCost)
    nb = 0
    while not seemsNotBad(newShip) and nb < 50:
        deleteShip(newShip)
        newShip = createRandomShip(maxCost)
        nb += 1
    return newShip


def seemsNotBad(ship):
    shipN, shipT = extractShipNameTypeFromFileName(ship)
    systemsUpgrades1, weaponsAdded1, dronesAdded1, energyAdded1 = extractInfos(ship)
    systemsUpgrades2, weaponsAdded2, dronesAdded2, energyAdded2 = extractBasicInfos(shipN, shipT)

    weaponsAdded, dronesAdded = weaponsAdded1+weaponsAdded2, dronesAdded1+dronesAdded2
    energyAdded = energyAdded1+energyAdded2
    systemsUpgrades = {}
    for k in systemsUpgrades1:
        if k in systemsUpgrades2:
            systemsUpgrades[k] = systemsUpgrades2[k] + systemsUpgrades1[k]
        else:
            systemsUpgrades[k] = systemsUpgrades1[k]
    for k in systemsUpgrades2:
        if k not in systemsUpgrades2:
            systemsUpgrades[k] = systemsUpgrades2[k]

    if energyAdded < len(weaponsAdded) + len(dronesAdded) + len([k for k in systemsUpgrades]):
        return False

    lowTierShips = {'stealth': 'typeC typeB', 'slug': 'typeB', 'engiCruiser': 'typeB', 'kestrel': 'typeC',
                    'zoltan': 'typeC', 'rock': 'typeA', 'federation': 'typeB'}
    if shipN in lowTierShips and shipT in lowTierShips[shipN]:
        return False

    lowTierWeapons = ['breachBombII', 'ionStunner', 'hull', 'fireBeam', 'chainIon', 'fireBomb', 'breach', 'heavyIon',
                      'hullLaserII', 'hullBeam', 'breachBombI', 'antibioBeam', 'burstLaserIII']
    for w in weaponsAdded:
        if w in lowTierWeapons:
            return False

    lowTiersDrones = ['ionIntruder', 'shieldOvercharger']
    for d in dronesAdded:
        if d in lowTiersDrones:
            return False

    return True


if __name__ == '__main__':
    print(multipleOptimization(500, 4, 4, nbInitGeneticAlgo=3))