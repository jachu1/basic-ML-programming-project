import numpy
import random
import sys

def policy_iteration(chooseEast, chooseNorth, chooseSouth, chooseWest, rewards):
#Iterate and loop here
    actions = ["EAST", "NORTH", "SOUTH", "WEST"]
    gamma = 0.99
    U = [0 for x in range(81)]
    pi = []

    for i in range(81):
        pi.append(random.choice(actions))

    while True:
        U = policy_evaluation(pi, gamma, chooseEast, chooseNorth, chooseSouth, chooseWest, rewards)
        temp = True

        for s in range(81):
            m = getMax(s, chooseEast, chooseNorth, chooseSouth, chooseWest, U)
            if m[0] > getV(s, pi, chooseEast, chooseNorth, chooseSouth, chooseWest, U):
                pi[s] = m[1]
                temp = False

        if temp:
            for i in range(80, -1, -1):
                if U[i] <= 0:
                    pi[i] = ""
            return pi

def getV(state, pi, chooseEast, chooseNorth, chooseSouth, chooseWest, prevUtilities):
#Utility of the current state
    sum = 0
    for s_ in range(81):
        if pi[state] == "EAST":
            sum += chooseEast[state][s_] * prevUtilities[s_]
        elif pi[state] == "NORTH":
            sum += chooseNorth[state][s_] * prevUtilities[s_]
        elif pi[state] == "SOUTH":
            sum += chooseSouth[state][s_] * prevUtilities[s_]
        elif pi[state] == "WEST":
            sum += chooseWest[state][s_] * prevUtilities[s_]

    return sum

def policy_evaluation(pi, gamma, chooseEast, chooseNorth, chooseSouth, chooseWest, rewards):
#Evaluate policy
    a = numpy.empty([81,81])
    b = numpy.empty(81)
    for s in range(81):
        a_ = []
        for s_ in range(81):
            temp = 0
            if pi[s] == "EAST":
                temp = (-1 * gamma * chooseEast[s][s_])
            elif pi[s] == "NORTH":
                temp = (-1 * gamma * chooseNorth[s][s_])
            elif pi[s] == "SOUTH":
                temp = (-1 * gamma * chooseSouth[s][s_])
            elif pi[s] == "WEST":
                temp = (-1 * gamma * chooseWest[s][s_])
            if s == s_:
                temp = 1 + temp
            a_.append(temp)
        a[s] = a_
        b[s] = rewards[s]

    return numpy.linalg.solve(a,b).tolist()

def getMax(s, chooseEast, chooseNorth, chooseSouth, chooseWest, values):
#Best state to go to
    east = 0
    north = 0
    south = 0
    west = 0
    for x in range(81):
        east += chooseEast[s][x] * values[x]
        north += chooseNorth[s][x] * values[x]
        south += chooseSouth[s][x] * values[x]
        west += chooseWest[s][x] * values[x]

    return max((east, "EAST"), (north, "NORTH"), (south, "SOUTH"), (west, "WEST"))

def optimize(pi):
#Put together policy object
    res = []

    for x in range(81):
        if pi[x] != "":
           res.append((x + 1, pi[x]))

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

    P = policy_iteration(chooseEast, chooseNorth, chooseSouth, chooseWest, rewards)
    pi = optimize(P)

    for x in pi:
        print x