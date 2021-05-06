#!/usr/bin/python

import threading
import time

import numpy as np
import json
import datetime
import multiprocessing

exitFlag = 0


def levenshtein_ratio_and_distance(s, t, ratio_calc=False):
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
    distance = np.zeros((rows, cols), dtype=int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row - 1] == t[col - 1]:
                cost = 0  # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
                                     distance[row][col - 1] + 1,  # Cost of insertions
                                     distance[row - 1][col - 1] + cost)  # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return distance[row][col]


def genomediff(x, y):
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
    if lenx < leny:
        swapped = True
        count = leny - lenx

    final = 0
    for i in range(count + 1):
        usedx = x[i:leny + i]
        usedy = y
        if swapped:
            usedx = x
            usedy = y[i:leny + i]

        result2 = levenshtein_ratio_and_distance(usedx, usedy, True)
        if result2 > final:
            final = result2
    return final


def algorithm(species, i, return_dict):
    """
    go over every collumb of the row i
    :param species: [[name, genome]]
    :param i: row
    :param return_dict: dictionory
    :return: return_dict
    """
    toapend = []
    for j in range(i, len(species)):
        if species[i][0] == species[j][0]:
            toapend.append(1.0)
        else:
            answer = genomediff(species[i][1], species[j][1])
            toapend.append(answer)

        newts = datetime.datetime.now()

        print(i + 1, " said ", " i'm done with comparing ", j + 1 + -i, " from ", len(species) - i, " , the time is",
              newts.time())
    return_dict[species[i][0]] = toapend
    print(species[i][0], " ", toapend)
    return return_dict


if __name__ == "__main__":
    f = open('sequenties.json', )
    data = json.load(f)
    species = []
    for i in data['species']:
        specie = [i["name"], i["genome"]]
        species.append(specie)
    f.close()

    oldts = datetime.datetime.now()
    processes = []
    return_dict = multiprocessing.Manager().dict()
    ronny = [0,2,4,6,8,10,12,14,16,17,18,19,23,24,25,26,27,28]
    for i in ronny:
        print("start procces %i" % (i+1))
        p = multiprocessing.Process(target=algorithm, args=(species, i, return_dict))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    with open('result_ronny.json', 'w') as fp:
        json.dump(return_dict.copy(), fp)
    fp.close()
