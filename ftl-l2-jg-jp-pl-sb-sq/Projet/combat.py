from random import randint
from time import time
from globalVar import showShipStateEnd, printTK
from displayShip import *

"""
Generation module for fights between ships.
"""


def combat(ship1, ship2):
    """
    Do a battle between two ships.

    @param ship1: A ship built with the class Ship.
    @type ship1: Object of class Ship.
    @param ship2: A ship built with the class Ship.
    @type ship2: Object of class Ship.
    """
    t1 = time()
    increaseTimeGenStills = 1
    if printTK:
        increaseTimeGenStills = 100

    while not ship1.ko() and not ship2.ko() and len(ship1.getCrew()) > 0 and len(ship2.getCrew()) > 0 \
            and time()-t1 < (5*increaseTimeGenStills):
        ship1.cooldowns()
        ship2.cooldowns()

        if randint(1, 100) > 49:
            ship1.attackOpponent(ship2)
            if not ship2.ko():
                ship2.attackOpponent(ship1)
        else:
            ship2.attackOpponent(ship1)
            if not ship1.ko():
                ship1.attackOpponent(ship2)
        #print(ship1.getHP(), ship2.getHP())

    if showShipStateEnd:
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print(displayInfosBoth(ship1, ship2))

    if ship1.ko() or len(ship1.getCrew()) == 0 or ship1.getHP() < ship2.getHP():
        # print('Ship '+ship2.getName()+' '+ship2.getType()+' ('+str(ship2.getID())+') won')
        return 'Ship 2 won'
    else:
        # print('Ship '+ship1.getName()+' '+ship1.getType()+' ('+str(ship1.getID())+') won')
        return 'Ship 1 won'