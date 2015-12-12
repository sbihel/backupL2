from geneticAlgorithm import *
from subprocess import call
from sys import platform as _platform


def buildLCMInputFile(listShips):
    """

    @param listShips: Like 'kestrelA0.xml'
    """
    if 'xmlShips' in os.getcwd() or 'pictures' in os.getcwd():
        os.chdir('..')
    nameF = 'inputLCM'
    while nameF in os.listdir():
        nameF += '2'
    with open(nameF, 'w') as fileTransitions:
        for shipF in listShips:
            tree = ET.parse('xmlShips/'+shipF)
            root = tree.getroot()

            shipN = root.findall('name')[0].text
            shipT = root.findall('type')[0].text
            systemsUpgrades1, weaponsAdded1, dronesAdded1, energyAdded1 = extractInfos(shipF)
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

            if energyAdded > 0:  # 0-30
                for i in range(energyAdded):
                    fileTransitions.write(str(i+1)+' ')

            if systemsUpgrades != {}:  # 31-179
                numberSystem = {'shields': 3, 'engines': 4, 'weaponControl': 5, 'oxygen': 6, 'medbay': 7,
                                'cloneBay': 8, 'droneControl': 9, 'hacking': 10, 'mindControl': 11,
                                'crewTeleporter': 12, 'cloaking': 13, 'piloting': 14, 'sensors': 15,
                                'doorSystem': 16, 'backupBattery': 17}
                for s in systemsUpgrades:
                    for i in range(systemsUpgrades[s]):
                        fileTransitions.write(str(numberSystem[s])+str(i+1)+' ')

            if weaponsAdded:  # 1001-1030
                weapons = [('leto', 20, 1), ('artemisPL', 38, 1), ('hermes', 45, 3), ('pegasus', 60, 3),
                           ('breach', 65, 3), ('hull', 65, 2), ('miniBeam', 20, 1), ('pikeBeam', 55, 2),
                           ('halberdBeam', 65, 3), ('glaiveBeam', 95, 4), ('fireBeam', 50, 2), ('hullBeam', 70, 2),
                           ('antibioBeam', 50, 2), ('basicLaser', 20, 1), ('dualLaser', 25, 1),
                           ('burstLaserI', 50, 2), ('burstLaserII', 80, 2), ('burstLaserIII', 95, 4),
                           ('heavyPierceI', 55, 2), ('heavyLaserI', 55, 1), ('heavyLaserII', 65, 3),
                           ('hullLaserI', 55, 2), ('hullLaserII', 75, 3), ('ionBlastI', 30, 1),
                           ('ionBlastII', 70, 3), ('heavyIon', 45, 2), ('ionStunner', 35, 1)]
                for w in weaponsAdded:
                    for indexX in range(len(weapons)):
                        if weapons[indexX][0] == w:
                            numberW = indexX
                    fileTransitions.write(str(1001+numberW)+' ')
            if dronesAdded:  # 1101-1120
                drones = [('combat1', 50, 2), ('combat2', 75, 4), ('beam1', 50, 2), ('beam2', 60, 3),
                          ('beamFire', 50, 3)]
                for d in dronesAdded:
                    for indexX in range(len(drones)):
                        if drones[indexX][0] == d:
                            numberD = indexX
                    fileTransitions.write(str(1101+numberD)+' ')
            fileTransitions.write('\n')
        fileTransitions.write('[EOF]')
    return nameF


def getBestFeatures(fileLCM):
    cwd = os.getcwd()
    rootF = cwd.split('Projet')[0]
    os.chdir(rootF+'lcm21/')
    if _platform == "win32":
        return 0
    else:
        call(['make'])
        print('\033[32m'+"Don't worry, it's ok. It's just warnings."+'\033[0m')
    nameF = 'outputLCM'
    while nameF in os.listdir('../Projet'):
        nameF += '2'
    if _platform == "win32":
        return 0
    else:
        try:
            call(['./fim_closed', '../Projet/'+fileLCM, '1', '../Projet/'+nameF])
        except:
            if not os.path.exists('../Projet/'+nameF):
                call(['./fim_closed', '../Projet/'+fileLCM, '1', '../Projet/'+nameF], shell=True)
            if not os.path.exists('../Projet/'+nameF):
                call(['./fim_closed.exe', '../Projet/'+fileLCM, '1', '../Projet/'+nameF])
    # call(['cp', '../Projet/'+fileLCM, '../Projet'+'TESTSTART'+fileLCM])
    # cleanLCMoutput('../Projet/'+nameF)
    orderLCMoutput('../Projet/'+nameF)
    translateLCMoutput(rootF+'Projet/'+nameF+'sorted')
    os.chdir(cwd)
    return nameF+'sorted'+'translated'


def translateLCMoutput(pathF):
    newF = ''
    with open(pathF) as lcmO:
        line = lcmO.readline()
        while line != '':
            for num in line.split('(')[0].split(' ')[:-1]:
                newF += translateNumber(num) + ' '
            newF += '(' + line.split('(')[1]
            line = lcmO.readline()
    with open(pathF+'translated', 'w') as lcmO:
        lcmO.write(newF)


def translateNumber(num):
    numI = int(num)
    if 0 <= numI <= 30:
        return 'energy'+num
    if 31 <= numI <= 179:
        numberSystem = {3: 'shields', 4: 'engines', 5: 'weaponControl', 6: 'oxygen', 7: 'medbay',
                        8: 'cloneBay', 9: 'droneControl', 10: 'hacking', 11: 'mindControl',
                        12: 'crewTeleporter', 13: 'cloaking', 14: 'piloting', 15: 'sensors',
                        16: 'doorSystem', 17: 'backupBattery'}
        return numberSystem[int(num[:-1])]+num[-1]
    if 1001 <= numI <= 1040:
        for w in range(len(weaponsSupported)):
            if w == numI-1001:
                return weaponsSupported[w][0]
    if 1101 <= numI <= 1120:
        for d in range(len(dronesSupported)):
            if d == numI - 1101:
                return dronesSupported[d][0]
    return ''


def orderLCMoutput(filePath):
    newF = ''
    tableLCM = []
    with open(filePath) as lcmO:
        for line in lcmO:
            numberAppereance = int(line.split('(')[1].split(')')[0])
            while len(tableLCM) < numberAppereance:
                tableLCM += [[]]
            tableLCM[numberAppereance-1] += [line]
    for iT in range(len(tableLCM)):
        for j in tableLCM[-iT-1]:
            newF += j
    with open(filePath+'sorted', 'w') as lcmOs:
        lcmOs.write(newF)


def cleanLCMoutput(filePath):
    """
    Keep only the line who doesn't have holes in systems/energy upgrades.

    @example:
    "engines1 engines2" is kept
    "engines2" isn't kept
    """
    # costs = {'energy': [30]*5 + [20]*5 + [25]*5 + [30]*5 + [35]*5,
    #          'shields': [125, 100, 20, 30, 40, 60, 80, 100],
    #          'engines': [0, 10, 15, 30, 40, 60, 80, 120],
    #          'weaponControl': [0, 40, 25, 35, 50, 75, 90, 100],
    #          'oxygen': [0, 25, 50],
    #          'medbay': [60, 35, 45],
    #          'cloneBay': [55, 35, 45],
    #          'droneControl': [35, 0, 20, 30, 45, 60, 80, 100],
    #          'hacking': [80, 35, 60],
    #          'mindControl': [75, 30, 60],
    #          'crewTeleporter': [90, 30, 60],
    #          'cloaking': [150, 30, 50],
    #          'piloting': [0, 20, 50],
    #          'sensors': [40, 25, 40],
    #          'doorSystem': [60, 35, 50],
    #          'backupBattery': [35, 50]}
    res = ''
    with open(filePath) as lcmO:
        for line in lcmO:
            keepIt = True
            lineT = line.split('(')[0].split(' ')[:-1]
            for w in lineT:
                nb = int(w)
                if 1 < nb <= 20:
                    for i in range(nb-1):
                        if str(i+1) not in lineT:
                            keepIt = False
                            break
                elif 21 <= nb <= 169 and nb % 10 > 1:
                    for i in range((nb % 10) - 1):
                        if w[:-1]+str(i+1) not in lineT:
                            keepIt = False
                            break
            # lineT = [translateNumber(w) for w in line.split('(')[0].split(' ')[:-1]]
            # for w in lineT:
            #     nbEnd = ''
            #     for i in range(len(w)):
            #         if w[len(w)-1-i] in '1234567890':
            #             nbEnd = w[len(w)-1-i] + nbEnd
            #         else:
            #             break
            #     if not nbEnd:
            #         continue
            #     if w[:-len(nbEnd)] in costs and int(nbEnd) > 1:
            #         for i in range(int(nbEnd)-1):
            #             if w[:-len(nbEnd)]+str(i+1) not in lineT:
            #                 keepIt = False
            if keepIt:
                res += line
            # print('lel')
    with open(filePath, 'w') as lcmO:
        lcmO.write(res)


def translateOneLineLCM(line):
    costs = {'energy': [30]*5 + [20]*5 + [25]*5 + [30]*5 + [35]*5,
             'shields': [125, 100, 20, 30, 40, 60, 80, 100],
             'engines': [0, 10, 15, 30, 40, 60, 80, 120],
             'weaponControl': [0, 40, 25, 35, 50, 75, 90, 100],
             'oxygen': [0, 25, 50],
             'medbay': [60, 35, 45],
             'cloneBay': [55, 35, 45],
             'droneControl': [35, 0, 20, 30, 45, 60, 80, 100],
             'hacking': [80, 35, 60],
             'mindControl': [75, 30, 60],
             'crewTeleporter': [90, 30, 60],
             'cloaking': [150, 30, 50],
             'piloting': [0, 20, 50],
             'sensors': [40, 25, 40],
             'doorSystem': [60, 35, 50],
             'backupBattery': [35, 50]}
    weapons = [('leto', 20, 1), ('artemisPL', 38, 1), ('hermes', 45, 3), ('pegasus', 60, 3), ('breach', 65, 3),
               ('hull', 65, 2), ('miniBeam', 20, 1), ('pikeBeam', 55, 2), ('halberdBeam', 65, 3), ('glaiveBeam', 95, 4),
               ('fireBeam', 50, 2), ('hullBeam', 70, 2), ('antibioBeam', 50, 2), ('basicLaser', 20, 1),
               ('dualLaser', 25, 1), ('burstLaserI', 50, 2), ('burstLaserII', 80, 2), ('burstLaserIII', 95, 4),
               ('heavyPierceI', 55, 2), ('heavyLaserI', 55, 1), ('heavyLaserII', 65, 3), ('hullLaserI', 55, 2),
               ('hullLaserII', 75, 3), ('ionBlastI', 30, 1), ('ionBlastII', 70, 3), ('heavyIon', 45, 2),
               ('ionStunner', 35, 1)]
    drones = [('combat1', 50, 2), ('combat2', 75, 4), ('beam1', 50, 2), ('beam2', 60, 3), ('beamFire', 50, 3)]
    line = line.split('(')[0][:-1].split(' ')
    systemsUpgrades = {}
    energyAdded = 0
    weaponsAdded, dronesAdded = [], []
    for w in line:
        if 'energy' in w:
            amount = int(w.split('energy')[1])
            if energyAdded < amount:
                energyAdded = amount
            continue
        for k in costs:
            if k in w:
                amount = int(w.split(k)[1])
                if k not in systemsUpgrades or systemsUpgrades[k] < amount:
                    systemsUpgrades[k] = amount
                break
        for weapon in [wpn[0] for wpn in weapons]:
            if weapon == w:
                weaponsAdded += [weapon]
                break
        for drone in [drn[0] for drn in drones]:
            if drone == w:
                dronesAdded += [drone]
                break
    return systemsUpgrades, weaponsAdded, dronesAdded, energyAdded


def addingToShipFromLCMLine(lineLCM, shipName, shipType):
    systemsUpgrades1, weaponsAdded1, dronesAdded1, energyAdded1 = translateOneLineLCM(lineLCM)

    if 'xmlShips' not in os.getcwd():
        tree1 = ET.parse('ftl_ships_layouts.xml')
    else:
        tree1 = ET.parse('../'+'ftl_ships_layouts.xml')
    root1 = tree1.getroot()
    if 'type' in shipType:
        ship = root1.findall(shipName)[0].findall(shipType)[0]
    else:
        ship = root1.findall(shipName)[0].findall('type'+shipType)[0]
    systemsUpgrades, weaponsPurchased, dronesPurchased, energyPurchased = {}, [], [], 0

    for s in systemsUpgrades1:
        if not ship.findall('systems')[0].findall(s):
            systemsUpgrades[s] = systemsUpgrades1[s]
        elif systemsUpgrades1[s] > int(ship.findall('systems')[0].findall(s)[0].text):
            systemsUpgrades[s] = systemsUpgrades1[s] - int(ship.findall('systems')[0].findall(s)[0].text)

    for w in weaponsAdded1:
        if w not in [n.text for n in ship.findall('weapons')[0]]:
            weaponsPurchased += [w]
        elif len([wpn for wpn in weaponsPurchased if wpn == w]) + \
            len([wpn for wpn in [n.text for n in ship.findall('weapons')[0]] if wpn == w]) < \
                len([wpn for wpn in weaponsAdded1 if wpn == w]):
            weaponsPurchased += [w]

    for d in dronesAdded1:
        if d not in [n.text for n in ship.findall('drones')[0]]:
            dronesPurchased += [d]
        elif len([wpn for wpn in dronesPurchased if wpn == d]) + \
            len([wpn for wpn in [n.text for n in ship.findall('drones')[0]] if wpn == d]) < \
                len([wpn for wpn in dronesAdded1 if wpn == d]):
            dronesPurchased += [d]

    if int(ship.findall('energy')[0].text) < energyAdded1:
        energyPurchased = energyAdded1 - int(ship.findall('energy')[0].text)

    return systemsUpgrades, weaponsPurchased, dronesPurchased, energyPurchased


def bestFeaturesNotInWorstFeatures(bestFeaturesF, worstFeaturesF, nbChampions, nbNoobs):
    """
    Take the best features that aren't in the worst features.
    """
    bF = []
    with open(bestFeaturesF) as bFF:  # BFF forever
        for linebF in bFF:
            bF += [(linebF.split(' ')[:-1], int(linebF.split('(')[1].split(')')[0]))]
    if not bF[0][0]:
        bF.pop(0)
    wF = []
    with open(worstFeaturesF) as wFF:
        for linewF in wFF:
            wF += [(linewF.split(' ')[:-1], int(linewF.split('(')[1].split(')')[0]))]
    if not wF[0][0]:
        wF.pop(0)
    nameFileRes = 'uniqueBestFeatures'
    while nameFileRes in os.listdir():
        nameFileRes += '2'

    finalBestFeatures = []
    wFeatOnly = [feature[0] for feature in wF]
    bFeatOnly = [feature[0] for feature in bF]
    for feature in bFeatOnly:
        # feature not sub set of too much worst features and sub set of some best features
        minRNoobs = 3 * nbNoobs / 4
        maxRChamp = nbChampions / 8
        superSetsNoobs = [lF for lF in wFeatOnly if testSubsetFeatures(feature, lF)]
        superSetChamps = [lF for lF in bFeatOnly if testSubsetFeatures(feature, lF)]
        if len(superSetsNoobs) < minRNoobs and len([superSetChamps]) > maxRChamp:
            finalBestFeatures += [feature]

    finalBestFeaturesNoSubset = []
    for feature in finalBestFeatures:
        if not [f for f in finalBestFeatures if f != feature and testSubsetFeatures(feature, f)]:
            finalBestFeaturesNoSubset += [feature[:]]

    if not finalBestFeaturesNoSubset:
        finalBestFeaturesNoSubset = [bF[i][0] for i in range(4)]
    res = ''
    for feature in finalBestFeaturesNoSubset:
        res += ' '.join(feature) + '\n'
    with open(nameFileRes, 'w') as resF:
        resF.write(res)
    return nameFileRes


def testSubsetFeatures(lFeatures1, lFeatures2):
    """
    Test if a list of features is a subset of anther one.
    """
    for feature in lFeatures1:
        if feature not in lFeatures2:
            return False
    return True


# def bestFeaturesFromGrowthRate(oldChampions, nbChampions):
#     """
#     @param oldChampions: List of list of champions from some genetic algorithms for example.
#     """
#     nameFileRes = 'growthBestFeatures'
#     ls = os.listdir()
#     while nameFileRes in ls:
#         nameFileRes += '2'
#     res = ''
#
#     for lC in oldChampions:
#         fileLCMinput = buildLCMInputFile(lC)
#         features = []
#         with open(fileLCMinput) as iLCM:
#             for lineI in iLCM:
#                 features += [translateOneLineLCM(lineI)]
#
#         initFeatures = [f[:] for f in features[nbChampions]]
#         newFeatures = []
#         for indexC in range(len(features)-nbChampions):
#             for f in features[indexC + nbChampions]:
#                 if f not in initFeatures:
#                     newFeatures += [f]
#
#         os.remove(fileLCMinput)
#
#     with open(nameFileRes, 'w') as growthRateFeatures:
#         growthRateFeatures.write(res)
#     return nameFileRes

def bestFeaturesFromGrowthRate(allFeaturesF, goodShips, badShips):
    nameFileRes = 'growthBestFeatures'
    ls = os.listdir()
    while nameFileRes in ls:
        nameFileRes += '2'
    res = ''

    featuresGoodShips = [infosToLine(*extractAllInfos(ship)) for ship in goodShips]
    featuresBadShips = [infosToLine(*extractAllInfos(ship)) for ship in badShips]

    with open(allFeaturesF) as allF:
        for feature in allF:
            nbApparitionsBad = len([f for f in featuresBadShips if testSubsetFeatures(feature, f)])
            nbApparitionsGood = len([f for f in featuresGoodShips if testSubsetFeatures(feature, f)])
            try:
                growthRate = (nbApparitionsGood / len(goodShips)) / (nbApparitionsBad / len(badShips))
            except ZeroDivisionError:
                growthRate = (nbApparitionsGood / len(goodShips)) / (1 / (len(badShips)*len(badShips)))
            trustGrowthRate = growthRate / (growthRate + 1)
            if trustGrowthRate > 0.33:
                res += feature

    with open(nameFileRes, 'w') as growthRateFeatures:
        growthRateFeatures.write(res)
    return nameFileRes


def infosToLine(systemsUpgrades, weaponsAdded, dronesAdded, energyAdded):
    res = ''
    if energyAdded > 0:  # 0-20
        for i in range(energyAdded):
            res += str(i+1)+' '

    if systemsUpgrades != {}:  # 21-169
        numberSystem = {'shields': 2, 'engines': 3, 'weaponControl': 4, 'oxygen': 5, 'medbay': 6,
                        'cloneBay': 7, 'droneControl': 8, 'hacking': 9, 'mindControl': 10,
                        'crewTeleporter': 11, 'cloaking': 12, 'piloting': 13, 'sensors': 14,
                        'doorSystem': 15, 'backupBattery': 16}
        for s in systemsUpgrades:
            for i in range(systemsUpgrades[s]):
                res += str(numberSystem[s])+str(i+1)+' '

    if weaponsAdded:  # 1001-1030
        weapons = [('leto', 20, 1), ('artemisPL', 38, 1), ('hermes', 45, 3), ('pegasus', 60, 3),
                   ('breach', 65, 3), ('hull', 65, 2), ('miniBeam', 20, 1), ('pikeBeam', 55, 2),
                   ('halberdBeam', 65, 3), ('glaiveBeam', 95, 4), ('fireBeam', 50, 2), ('hullBeam', 70, 2),
                   ('antibioBeam', 50, 2), ('basicLaser', 20, 1), ('dualLaser', 25, 1),
                   ('burstLaserI', 50, 2), ('burstLaserII', 80, 2), ('burstLaserIII', 95, 4),
                   ('heavyPierceI', 55, 2), ('heavyLaserI', 55, 1), ('heavyLaserII', 65, 3),
                   ('hullLaserI', 55, 2), ('hullLaserII', 75, 3), ('ionBlastI', 30, 1),
                   ('ionBlastII', 70, 3), ('heavyIon', 45, 2), ('ionStunner', 35, 1)]
        for w in weaponsAdded:
            for indexX in range(len(weapons)):
                if weapons[indexX][0] == w:
                    numberW = indexX
            res += str(1001+numberW)+' '
    if dronesAdded:  # 1101-1120
        drones = [('combat1', 50, 2), ('combat2', 75, 4), ('beam1', 50, 2), ('beam2', 60, 3),
                  ('beamFire', 50, 3)]
        for d in dronesAdded:
            for indexX in range(len(drones)):
                if drones[indexX][0] == d:
                    numberD = indexX
            res += str(1101+numberD)+' '

    return res

if __name__ == '__main__':
    # with open('ExampleoutputLCMtranslated') as oP:
    #     for lineT in oP:
    #         print(lineT, translateOneLineLCM(lineT))
    #
    # with open('ExampleoutputLCMtranslated') as oP:
    #     for i in range(1):
    #         oP.readline()
    #     print(addingToShipFromLCMLine(oP.readline(), 'engiCruiser', 'A'))

    print(getBestFeatures(buildLCMInputFile(['kestrelC1.xml', 'kestrelA1.xml', 'engiCruiserA2.xml'])))