from combat import *
from time import time
from variousShips import *
from random import seed

"""
test for various fights
"""
##
##
##def nfight(n):
##    """
##    n fights of 2 Kestrel A
##    """
##    ship1Won = 0
##    t1 = time()
##    for k in range(n):
##        ship1 = genShip()
##        ship2 = genShip()
##        ship1.getSystem('weaponControl').powerWeapon(0)
##        ship2.getSystem('weaponControl').powerWeapon(0)
##        ship1.getSystem('weaponControl').powerWeapon(1)
##        ship2.getSystem('weaponControl').powerWeapon(1)
##        ship1.getSystem('shields').addPower(2)
##        ship2.getSystem('shields').addPower(2)
##        ship1.getSystem('piloting').addPower(1)
##        ship2.getSystem('piloting').addPower(1)
##        ship1.getSystem('engines').addPower(1)
##        ship2.getSystem('engines').addPower(1)
##        ship1.getSystem('weaponControl').addWeapon(genWeapon('dualLaser'))
##        ship1.getSystem('weaponControl').powerWeapon(2)
##        if combat(ship1, ship2) == 'Ship 1 won':
##            ship1Won += 1
##    t2 = time()
##    print('Ship 1 won '+str(ship1Won)+' times on '+str(n))
##    print('Round time : '+str((t2-t1)/n)+' seconds per fight')


def nfight(mafonction):
    def wrapper(n):
        ship1Won = 0
        t1 = time()
        for i in range(n):
            ship1, ship2 = mafonction()
            if combat(ship1, ship2) == 'Ship 1 won':
                ship1Won += 1
        t2 = time()
        print('Ship 1 won '+str(ship1Won)+' times on '+str(n))
        print('Round time : '+str((t2-t1)/n)+' seconds per fight')
    return wrapper


@nfight
def KestrelAvsKestrelA():
    """
    1 fight between 2 Kestrel =
    """
    ship1 = genShip(1)
    ship2 = genShip(2)
    ship1.hasSystem('weaponControl')
    ship1.getSystem('weaponControl').powerWeapon(0)
    ship2.getSystem('weaponControl').powerWeapon(0)
    ship1.getSystem('weaponControl').powerWeapon(1)
    ship2.getSystem('weaponControl').powerWeapon(1)
    ship1.getSystem('shields').addPower(2)
    ship2.getSystem('shields').addPower(2)
    ship1.getSystem('piloting').addPower(1)
    ship2.getSystem('piloting').addPower(1)
    ship1.getSystem('engines').addPower(1)
    ship2.getSystem('engines').addPower(1)
    return ship1, ship2


@nfight
def KestrelAvsKestrelB():
    ship1 = genShip(1)
    ship2 = genShip(2, 'kestrel', 'typeB')
    ship1.hasSystem('weaponControl')
    ship1.getSystem('weaponControl').powerWeapon(0)
    ship2.getSystem('weaponControl').powerWeapon(0)
    ship1.getSystem('weaponControl').powerWeapon(1)
    ship2.getSystem('weaponControl').powerWeapon(1)
    ship1.getSystem('shields').addPower(2)
    ship2.getSystem('shields').addPower(2)
    ship1.getSystem('piloting').addPower(1)
    ship2.getSystem('piloting').addPower(1)
    ship1.getSystem('engines').addPower(1)
    ship2.getSystem('engines').addPower(1)
    ship2.getSystem('weaponControl').powerWeapon(2)
    return ship1, ship2


@nfight
def KestrelBvsEngiCruiser():
    ship5 = genShip(1, 'kestrel', 'typeB')
    ship5.getSystem('weaponControl').powerWeapon(0)
    ship5.getSystem('weaponControl').powerWeapon(1)
    ship5.getSystem('shields').addPower(2)
    ship5.getSystem('piloting').addPower(1)
    ship5.getSystem('engines').addPower(1)
    ship5.getSystem('weaponControl').addWeapon(genWeapon('burstLaserI'))
    ship5.getSystem('weaponControl').powerWeapon(2)

    ship6 = genShip(2, 'engiCruiser')
    ship6.getSystem('weaponControl').powerWeapon(0)
    ship6.getSystem('droneControl').powerDrone(0)
    ship6.getSystem('shields').addPower(2)
    ship6.getSystem('piloting').addPower(1)
    ship6.getSystem('engines').addPower(1)

    return ship5, ship6


@nfight
def test():
    s1 = extractShip('kestrel', 'typeA', '0', 1)
    s2 = extractShip('engiCruiser', 'typeA', '1', 2)
    return s1, s2

#seed(1192)

#KestrelAvsKestrelB(5)
test(5)
