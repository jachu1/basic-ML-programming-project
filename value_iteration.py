import numpy
import random
import sys

def getV(chooseEast, chooseNorth, chooseSouth, chooseWest, rew):
#Utility of the current state
    gamma = 0.99
    U = [0 for x in range(81)]
    UP = [0 for x in range(81)]

    while True:
        U = UP[:]
        delta = 0
        for s in range(81):
            UP[s] = rew[s] + (gamma * getMax(s, chooseEast, chooseNorth, chooseSouth, chooseWest, U))
            if abs(UP[s] - U[s]) > delta:
                delta = abs(UP[s] - U[s])
        if delta == 0:
            break

    return U

def getMax(state, chooseEast, chooseNorth, chooseSouth, chooseWest, values):
#Best state to go to
    east = 0
    north = 0
    south = 0
    west = 0
    for x in range(81):
        east += chooseEast[state][x] * values[x]
        north += chooseNorth[state][x] * values[x]
        south += chooseSouth[state][x] * values[x]
        west += chooseWest[state][x] * values[x]

    return max(east, north, south, west)

def optimize(chooseEast, chooseNorth, chooseSouth, chooseWest, values):
#Put together policy object
    res = [0 for x in range(81)]

    for x in range(81): #Trickle-back calculations
        east = 0
        north = 0
        south = 0
        west = 0
        for y in range(81):
            east += chooseEast[x][y] * values[y]
            north += chooseNorth[x][y] * values[y]
            south += chooseSouth[x][y] * values[y]
            west += chooseWest[x][y] * values[y]
        act = max((east, "EAST"),(north, "NORTH"),(south, "SOUTH"),(west, "WEST"))
        res[x] = (x + 1, values[x], act[1])

    for i in range(80, -1, -1):
        if res[i][1] <= 0:
            del res[i]

    return res

if __name__ == '__main__':
    f_open_e = open('prob_east.txt')
    f_open_n = open('prob_north.txt')
    f_open_s = open('prob_south.txt')
    f_open_w = open('prob_west.txt')
    f_open_rew = open('rewards.txt')
    chooseEast = []
    chooseNorth = []
    chooseSouth = []
    chooseWest = []
    rewards = []

    chooseEast = [[0.0 for x in xrange(81)] for y in xrange(81)]
    for line in f_open_e.readlines():
        s, s_, prob = map(float,line.strip().split())
        chooseEast[int(s) - 1][int(s_) - 1] = prob

    chooseNorth = [[0.0 for x in xrange(81)] for y in xrange(81)]
    for line in f_open_n.readlines():
        s, s_, prob = map(float,line.strip().split())
        chooseNorth[int(s) - 1][int(s_) - 1] = prob

    chooseSouth = [[0.0 for x in xrange(81)] for y in xrange(81)]
    for line in f_open_s.readlines():
        s, s_, prob = map(float,line.strip().split())
        chooseSouth[int(s) - 1][int(s_) - 1] = prob
    
    chooseWest = [[0.0 for x in xrange(81)] for y in xrange(81)]
    for line in f_open_w.readlines():
        s, s_, prob = map(float,line.strip().split())
        chooseWest[int(s) - 1][int(s_) - 1] = prob

    for line in f_open_rew.readlines():
        rewards.append(int(line.strip()))

    utils = getV(chooseEast, chooseNorth, chooseSouth, chooseWest, rewards)
    pi = optimize(chooseEast, chooseNorth, chooseSouth, chooseWest, utils)

    for x in pi:
        print x