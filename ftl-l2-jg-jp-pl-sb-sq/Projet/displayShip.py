import re
from globalVar import pausesCombat


def displayInfos(ship):
    s = '=============================================================\n'
    esp = '    '
    SBred = '\033[41m'
    SBgre = '\033[42m'
    Sgre = '\033[32m'
    Sred = '\033[31m'
    Sblue = '\033[34m'
    SBblue = '\033[44m'
    Smagenta = '\033[35m'
    Syel = '\033[33m'
    Syel2 = '\033[33m'
    SBblack = '\033[40m'
    End = '\033[0m'
    s += ship.getName() + ship.getType() + ' ID: '+str(ship.getID())+'\n'
    HP = ship.getHP()
    s += esp+'- HP: '+Sgre+str(HP)+'/30'+End+': '+str(int(HP)*(SBgre+' '+End))+str(int(30-HP)*(SBred+' '+End))+'  '
    if ship.hasSystem('shields'):
        shields = ship.getSystem('shields')
        l = shields.getLayers()
        s += '- Shields: ' + str(l*(SBblue+' '+End)) + \
             str(((shields.getCurrentMaxPower()//2)-l)*(SBblack+' '+End)) + '\n'
    else:
        s += '\n'
    s += esp+'- Energy available: '+str(ship.getPowerAvailable())+'/'+str(ship.getMaxPower()) + '\n'
    s += esp+'- Missiles: '+str(ship.getMissiles())+'  |  '+'Drone Parts: '+str(ship.getDroneParts())+'\n'
    s += esp+'- Systems :\n'
    res = '     '
    for sys in ship.getSystems():
        res += addSpaces(sys.getNameAbbreviation(), 10)
    res += '\nEnergy:'
    for sys in ship.getSystems():
        if sys.getCurrentMaxPower() < sys.getMaxPower():
            res += Sred+esp+' '+str(sys.getPowerInIt())+'/'+str(sys.getCurrentMaxPower())+End+'  '
        else:
            res += esp+' '+str(sys.getPowerInIt())+'/'+str(sys.getCurrentMaxPower())+'  '
    res = res[:-2]
    res += '\nIonised:  '
    for sys in ship.getSystems():
        if sys.isIonised():
            res += Sblue+addSpaces('True', 5)+End+'     '
        else:
            res += str(False)+'     '
    res = res[:-5]
    res += '\nRep:       '
    for sys in ship.getSystems():
        nbR = sys.getRepair()
        if nbR > 0:
            res += Syel+addSpaces(str(nbR), 3)+'%'+End+esp+'  '
        else:
            res += addSpaces(str(nbR), 3)+'%'+esp+'  '
    res = res[:-2-len(esp)]
    s += res + '\n'
    res = ''
    s += esp+'- Rooms :\n'
    res += 'Fires :    '
    for room in ship.getRooms():
        nbF = room.getFire()
        if nbF > 0:
            res += Sred+str(nbF)+End+'   '
        else:
            res += str(nbF)+'   '
    res = res[:-3]
    res += '\nBreaches : '
    for room in ship.getRooms():
        nbB = room.getBreach()
        if nbB > 0:
            res += Smagenta+str(nbB)+End+'   '
        else:
            res += str(nbB)+'   '
    res = res[:-3]
    res += '\n0xy  :   '
    for room in ship.getRooms():
        nbO = int(room.getOxygen())
        if nbO < 6:
            res += Syel2+addSpaces(str(nbO), 3)+End+' '
        else:
            res += addSpaces(str(nbO), 3)+' '
    res = res[:-1]
    s += res + '\n'
    s += esp+'- Crew : \n'
    for crew in ship.getCrew():
        s += str(crew) + '\n'
    s += esp+'- Weapons : \n'
    res = ''
    for w in ship.getSystem('weaponControl').getWeapons():
        res += '-' + str(w) + '\n'
    s += res
    if ship.hasSystem('droneControl'):
        res = esp+'- Drones: \n'
        for d in ship.getSystem('droneControl').getDrones():
            res += '-'+str(d)+'\n'
        s += res
    s += '============================================================='
    return s


def displayAttack(weapon, ship1, ship2, target):
    if pausesCombat:
        entry = input('Continue ? ')

    if weapon.getType() == 'beam' or ship2.getRooms()[target].getSystem() is False:
        targetDisplay = ' on ' + str(target)
    else:
        targetDisplay = ' on room ' + str(target) + ' (' + ship2.getRooms()[target].getSystem() + ')'

    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print('******',
          ship1.getName(), ship1.getType(), '(', str(ship1.getID()), ')', 'used ', weapon.getName(), targetDisplay,
          ' of ', ship2.getName(), ship2.getType(), '(', str(ship2.getID()), ')', '******\n',
          displayInfosBoth(ship1, ship2))


def displayInfosBoth(ship1, ship2):
    if ship2.getID() > ship1.getID():
        L = [displayInfos(ship1).split('\n'), displayInfos(ship2).split('\n')]
    else:
        L = [displayInfos(ship2).split('\n'), displayInfos(ship1).split('\n')]
    return str(InfosBoth(inverseStringList(L)))[1:]


def addSpaces(word, length):
    return (length - len(word))*' ' + word


def addSpacesEnd(word, length):
    return word + (length - len(word))*' '


def inverseStringList(L):
    new = [[''] * len(L) for i in range(maxLength(L))]
    for i in range(len(L)):
        for j in range(len(L[i])):
            new[j][i] = L[i][j]
    return new


def maxLength(L):
    maxi = 0
    for i in L:
        if len(i) > maxi:
            maxi = len(i)
    return maxi


class InfosBoth(list):

    def __init__(self, L):
        list.__init__(self, L)

    def __repr__(self):
        res = ''
        maxL = self.maxL1()
        for i in self:
            res += i[0] + (maxL-self.lenColorsString(i[0])) * ' ' + ' || ' + i[1] + '\n'
        return res

    def maxL1(self):
        maxi = 0
        for i in self:
            if self.lenColorsString(i[0]) > maxi:
                maxi = self.lenColorsString(i[0])
        return maxi

    def lenColorsString(self, s):
        ansi_escape = re.compile(r'\x1b[^m]*m')
        decodedString = ansi_escape.sub('', s)
        return len(decodedString)





