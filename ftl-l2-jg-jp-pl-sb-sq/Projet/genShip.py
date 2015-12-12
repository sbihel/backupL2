#!/usr/local/bin/python3

from variousShips import *
import sys
import getopt
import random

####################################
# s == seed
# w == weapons wanted list
####################################
myopts, args = getopt.getopt(sys.argv[1:], "s:w:")

scrapsValue = int(args[0])
seed = None
weaponsWanted = []

for index in range(len(args)):
    if args[index] == '-s':
        seed = int(args[index+1])
    elif args[index] == '-w':
        j = 1
        while index+j < len(args) and args[index+j][0] != '-':
            weaponsWanted += [args[index+j]]
            j += 1


random.seed(seed)
createRandomShip(scrapsValue, weaponsWanted=weaponsWanted)