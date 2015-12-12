from math import sqrt
from random import randint
from globalVar import *


class Room(object):
    """
    Class which allow you to monitor each room.
    """

    def __init__(self, kw, nb, doors):
        """
        @param kw: List of the holes, their position and the tuple of the 2 rooms they link.
        """
        self.__x1 = kw['coords'][0][0]
        self.__y1 = kw['coords'][0][1]
        self.__x2 = kw['coords'][1][0]
        self.__y2 = kw['coords'][1][1]
        self.__breach = 0
        self.__fire = 0
        self.__extinction = 0
        self.__repairBreach = 0
        self.__system = kw['system']  # name of the system that the room can have
        self.__hasSystem = kw['hasSystem']  # True if the room has a system now
        self.__doors = doors
        self.__nb = nb  # index number in the list in ship
        self.__oxygen = 0

    def getCoords(self):
        """
        Renvoie les coordonnees d'une salle
        @return: liste de deux points
        """
        return [[self.__x1, self.__y1], [self.__x2, self.__y2]]

    def getNbBoxes(self):
        """
        Return the number of boxes that compose the room, normally only 2 or 4.
        @return: Return the number of boxes composing the room.
        @rtype: Integer.
        """
        if self.__system == 'medbay' and self.__hasSystem:
            return 3
        return (sqrt((self.__x1-self.__x2)**2)/10)*(sqrt((self.__y1-self.__y2)**2)/10)

    def getDoors(self):
        return self.__doors

    def setDoors(self, d):
        self.__doors = d

    def getBreach(self):
        """
        Renvoie s'il y a une breche dans la coque
        @rtype: Integer
        """
        return self.__breach

    def doBreach(self):
        if self.__breach < self.getNbBoxes():
            self.__breach += 1

    def repairBreach(self):
        if self.__breach > 0:
            self.__breach -= 1

    def getFire(self):
        """
        Renvoie s'il y a du feu
        @rtype: Integer
        """
        return self.__fire

    def startFire(self):
        if self.__fire < self.getNbBoxes():
            self.__fire += 1

    def extinguishFire(self):
        if self.__fire > 0:
            self.__fire -= 1

    def getSystem(self):
        """
        @return: Return the name of the system that is in the room or False if there is no system.
        @rtype String or Boolean.
        """
        if self.__hasSystem and self.__system != '':
            return self.__system
        return False

    def hasSystem(self):
        """
        @return: Return the name of the system that is in the room or False if there is no system.
        @rtype String or Boolean.
        """
        return self.__hasSystem and self.__system != ''

    def getNB(self):
        return self.__nb

    def getOxygen(self):
        return self.__oxygen

    def setOxygen(self, nb):
        if nb > 100:
            self.__oxygen = 100
        elif nb < 0:
            self.__oxygen = 0
        else:
            self.__oxygen = nb

    def removeOxygen(self, nb):
        if self.__oxygen <= nb:
            self.__oxygen = 0
        else:
            self.__oxygen -= nb

    def addOxygen(self, nb):
        if self.__oxygen+nb >= 100:
            self.__oxygen = 100
        else:
            self.__oxygen += nb

    def cooldowns(self, crew, system, listRooms):
        """
        Fires, repair, boarders...
        """

        self.crewTasks(crew, system)

        crewIn = [k for k in crew if k.getRoom().getNB() == self.__nb]
        for k in crewIn:
            if k.getRace() == 'lanius':
                self.removeOxygen(5/divisionTime)  # same amount as a single breach

        self.dotsToCrew(crew)

        if self.__fire > 0 and self.__oxygen <= 5:  # suffocation of fires
            self.__extinction += self.__fire*50/divisionTime
            # extinction of fires are faster the more fire there is
            self.testExtinction()
            # extinction 1 by 1, normally there should be a var extinction for each fire
            # to get closer to this, we made the extinction faster the more fires there is

        if self.__breach > 0:
            self.removeOxygen(self.__breach * 7 / divisionTime)  # unknown stat
        if self.__fire > 0:
            if self.__hasSystem:
                system.dotFire(self.__fire)
            self.removeOxygen(2/divisionTime)  # unknown stat

        self.expansionFire(listRooms)
        self.expansionOxygen(listRooms)

    def crewTasks(self, crew, system):
        """
        The tasks crew members have to do each turn, like repair, extinguish fires...
        @param crew: List of the crew members of the entire ship.
        @type crew: List of objects of the class CrewMember.
        @param system: System in the room.
        @type system: Object of the class System, something else if there's no system.
        """
        crewIn = [k for k in crew if k.getRoom().getNB() == self.__nb and not k.isInMovement()]
        if crewIn is not []:
            if self.__fire > 0:  # priority to extinguish the fire
                for k in crewIn:  # unknown stats, only known that rate of extinguish is the lvl of repair
                    self.__extinction += k.getPercentageExtinction()/divisionTime
                    self.testExtinction()
            elif self.__breach > 0:
                for k in crewIn:
                    self.__repairBreach += k.getPercentageRepair()/divisionTime
                    self.testBreachRepair()
            elif self.__hasSystem:  # no fire or breach, can repair system
                system.reparation(crewIn)

    def dotsToCrew(self, crew):
        """
        Damages over time to the crewmen in the room, due to fire and suffocation.
        @param crew: List of the crew members of the entire ship.
        @type crew: List of objects of the class CrewMember.
        """
        if self.__oxygen <= 5:  # suffocation
            for k in [k for k in crew if k.getRoom().getNB() == self.__nb]:
                k.suffocation()
        if self.__fire > 0:  # crewmen take damages if they can't extinguish fires
            for k in [k for k in crew if k.getRoom().getNB() == self.__nb]:
                k.fireDamages(self.__fire)

    def testExtinction(self):
        if self.__extinction >= 100:
            self.__fire -= 1
            self.__extinction -= 100
        if self.__fire == 0:  # reset of the percentage of extinction
            self.__extinction = 0

    def testBreachRepair(self):
        if self.__repairBreach >= 100:
            self.__breach -= 1
            self.__repairBreach -= 100
        if self.__breach == 0:
            self.__breach = 0

    def expansionFire(self, listRooms):
        # completely unknown stats for this part
        maxFirePerTick = 0
        for i in range(self.__fire):
            if randint(1, 100) < 51/divisionTime:
                # random stat cause unknown, 50% chance of spreading each second
                for k in self.__doors:
                    if not k.isClosed() and randint(1, 100) < 25 and maxFirePerTick == 0:
                        if k.getLink()[0] != self.__nb:
                            listRooms[k.getLink()[0]].startFire()
                            maxFirePerTick = 1
                if maxFirePerTick == 0:
                    self.startFire()
                    maxFirePerTick = 1

    def expansionOxygen(self, listRooms):
        # also unknown stats...
        for k in self.__doors:
            if not k.isClosed():
                if -1 in k.getLink():
                    self.removeOxygen(15/divisionTime)
                else:
                    if k.getLink()[0] == self.__nb:
                        otherRoom = listRooms[k.getLink()[1]]
                    else:
                        otherRoom = listRooms[k.getLink()[0]]
                    if otherRoom.getOxygen() > self.__oxygen and otherRoom.getOxygen() > 5:
                        otherRoom.removeOxygen(5)
                        self.addOxygen(5)