#!/usr/bin/python

import threading
import time

import numpy as np
import json
import datetime
import multiprocessing
import functools
import ClientCodeclass



def makeMatrix(s):
    rows = s+1
    cols = s+1
    distance = np.zeros((rows, cols), dtype=int)
    # Populate matrix of zeros with the indeces of each character of both strings
    # for i in range(1, rows):
    #     for k in range(1, cols):
    #         distance[i][0] = i
    #         distance[0][k] = k
    for i in range(1, rows):
        distance[i][0] = i
    for k in range(1, cols):
        distance[0][k] = k
    return distance

# @functools.lru_cache(maxsize=None)
def levenshtein_ratio_and_distance(s, t, distance):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros

    rows = len(s) + 1
    cols = len(t) + 1
    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions

    print(f"start{datetime.datetime.now().time()}")
    for col in range(1, cols):
        for row in range(1, rows):

            cost = 2
            if s[row - 1] == t[col - 1]:
                cost = 0  # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
                                     distance[row][col - 1] + 1,  # Cost of insertions
                                     distance[row - 1][col - 1] + cost)  # Cost of substitutions
        # Computation of the Levenshtein Distance Ratio
    print(f"stop{datetime.datetime.now().time()}")

    Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
    return Ratio

def genomediff(x, y, client1, name):
    """
    calculate the diffrent combinations of the 2 genomes
    :param x: genome 1
    :param y: genome 2
    :return: best combination
    """
    lenx = len(x)
    leny = len(y)
    swapped = False

    count = lenx - leny
    smallest = leny
    longest = lenx
    start = 0
    final = 0

    if lenx < leny:
        longest = leny
        swapped = True
        count = leny - lenx
        smallest = lenx

    try:
        fi = open(f"{name}.json")
        dataname = json.load(fi)
        fi.close()
        if dataname["final"] == True:
            return dataname["result"]
        start = dataname["i"]
        final = dataname["result"]

    except (FileNotFoundError, IOError):
        if longest > 14000 and smallest <10000:
            start = 14100 - (smallest*2)
            count = min(count, 14200+smallest*2)
    distance = makeMatrix(smallest)

    step = 100
    steptotal = 0
    for i in range(start, count + 1):
        step += 1
        steptotal +=1
        usedx = x[i:leny + i]
        usedy = y
        if swapped:
            usedx = x
            usedy = y[i:lenx + i]
        result2 = levenshtein_ratio_and_distance(usedx, usedy, distance.copy())


        if result2 > final:
            final = result2
            client1.update(final, i, False)
            step = 0
        if step>=100:
            client1.update(final, i, False)
            step = 0
    client1.update(final, count, True)
    print(f"this were the steps {steptotal}")
    return final


def algorithm(species, i, return_dict):
    """
    go over every collumb of the row i
    :param species: [[name, genome]]
    :param i: row
    :param return_dict: dictionory
    :return: return_dict
    """
    toapend = [] # Lijst van resultaten van alle kolommen in volgorde
    for j in range(i, len(species)): # Loop over alle kolommen
        if j in [19, 24, 25, 26]:
            client1 = ClientCodeclass.clientclass(species[i][0], species[j][0]) # Client initializeren
            client1.ask() #
            if species[i][0] == species[j][0]:
                toapend.append(1.0)
            else:
                answer = genomediff(species[i][1], species[j][1], client1, f"{species[i][0]}{species[j][0]}")
                toapend.append(answer)
            client1.closee()
            newts = datetime.datetime.now()

            print(i + 1, " said ", " i'm done with comparing ", j + 1 + -i, " from ", len(species) - i, " , the time is",
                  newts.time())
    return_dict[species[i][0]] = toapend
    print(species[i][0], " ", toapend)
    return return_dict


def algorithm2(species, i):
    """
    go over every collumb of the row i
    :param species: [[name, genome]]
    :param i: row
    :param return_dict: dictionory
    :return: return_dict
    """
    toapend = [] # Lijst van resultaten van alle kolommen i
    client1 = ClientCodeclass.clientclass(species[i][0], species[j][0]) # Client initializeren
    client1.ask() #
    answer = genomediff(species[i][1], species[j][1], client1, f"{species[i][0]}{species[j][0]}")
    toapend.append(answer)
    client1.closee()
    newts = datetime.datetime.now()

    print(i + 1, " said ", " i'm done with comparing ", j + 1 + -i, " from ", len(species) - i, " , the time is",
          newts.time())


if __name__ == "__main__":
    f = open('sequenties.json')
    data = json.load(f)
    species = []
    for i in data['species']:
        specie = [i["name"], i["genome"]]
        species.append(specie)
    f.close()

    oldts = datetime.datetime.now()
    processes = []
    return_dict = multiprocessing.Manager().dict()
    ronny = [0, 2, 4, 6, 8, 10, 12, 14, 16, 17, 18, 19, 23, 24, 25, 26, 27, 28]
    donski = [5, 19, 24, 25]
    for i in donski:
        for j in range(i, len(species)):  # Loop over alle kolommen
            if j in [19, 24, 25, 26] and i!=j:
                print("start procces %i" % (i+1))
                p = multiprocessing.Process(target=algorithm2, args=(species, i))
                processes.append(p)
                p.start()

    for process in processes:
        process.join()

