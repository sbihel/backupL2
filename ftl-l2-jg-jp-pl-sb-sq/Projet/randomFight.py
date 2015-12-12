#!/usr/local/bin/python3

from fightsWithVariousShips import *

maxCost = 400
ship1 = createRandomShip(maxCost)
ship2 = createRandomShip(maxCost)

ship3 = extractShipFromFileName(ship1, ID=1)
ship4 = extractShipFromFileName(ship2, ID=2)

combat(ship3, ship4)
