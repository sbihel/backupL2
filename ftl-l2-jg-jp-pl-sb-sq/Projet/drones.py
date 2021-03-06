import os
import xml.etree.ElementTree as ET
if 'xmlShips' in os.getcwd():
    os.chdir('..')
tree = ET.parse('ftl_drones_resources.xml')
root = tree.getroot()


class Drone(object):

    def __init__(self, name, typeD, power, cost):
        self.__name = name
        self.__type = typeD
        self.__power = power
        self.__cost = cost
        self.__isPowered = False
        self.__cooldown = 0

    def __repr__(self):
        return 'Name: '+self.__name+'  Active: '+str(self.__isPowered)

    def getName(self):
        return self.__name

    def powerIt(self):
        self.__isPowered = True

    def unpowerIt(self):
        self.__isPowered = False

    def isPowered(self):
        return self.__isPowered

    def getPower(self):
        return self.__power

    def getCooldown(self):
        return self.__cooldown

    def setCooldown(self, val):
        self.__cooldown = val

    def getType(self):
        return self.__type


class CombatDrone(Drone):

    def __init__(self, name, power, cost, speed, length):
        Drone.__init__(self, name, 'combat', power, cost)
        self.__speed = speed
        self.__length = length

    def getSpeed(self):
        return self.__speed

    def getBeamLength(self):
        return self.__length

    def getDamage(self):
        return 1

    def getFireChance(self):
        return 1 * (self.getName() == 'beamFire')


class DefensiveDrone(Drone):

    def __init__(self, name, power, cost):
        Drone.__init__(self, name, 'defense', power, cost)


def genDrone(nameDrone):
    combatDrone = ['combat1', 'combat2', 'beam1', 'beam2', 'beamFire']
    if nameDrone in combatDrone:
        return genCombatDrone(nameDrone)

    defenseDrone = ['defense1', 'defense2', 'antiCombat', 'shieldOvercharger', 'shieldOverchargerP']
    if nameDrone in defenseDrone:
        return genDefenseDrone(nameDrone)


def genCombatDrone(nameDrone):
    return CombatDrone(name=nameDrone,
                       power=int(root.find('.//'+nameDrone+'/power').text),
                       cost=int(root.find('.//'+nameDrone+'/cost').text),
                       speed=int(root.find('.//'+nameDrone+'/speed').text),
                       length=int(root.find('.//'+nameDrone+'/length').text))


def genDefenseDrone(nameDrone):
    return DefensiveDrone(name=nameDrone,
                          power=int(root.find('.//'+nameDrone+'/power').text),
                          cost=int(root.find('.//'+nameDrone+'/cost').text))