#!/usr/bin/python

import threading
import time

import numpy as np
import json
import datetime
import multiprocessing
import functools
import ClientCodeclass
import Levenshtein

# @functools.lru_cache(maxsize=None)
def levenshtein_ratio_and_distance(s, t):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # print(f"number1 start{datetime.datetime.now().time()}")
    x = Levenshtein.ratio(s, t)
    # print(x)

    # print(f"number1 stop {datetime.datetime.now().time()}")
    return x




def genomediff(x, y, client1, name, request):
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

    if request != None:
        dataname = request
        if dataname["final"] == True:
            return dataname["result"]
        start = dataname["i"]
        final = dataname["result"]

    else:
        if longest > 14000 and smallest <10000:
            start = 14100 - (smallest*2)
            count = min(count, 14200+smallest*2)

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
        result2 = levenshtein_ratio_and_distance(usedx, usedy)
        # result3 = levenshtein_ratio_and_distance2(usedx, usedy, distance.copy())
        # print(f"{result2} vs {result3} = {result2-result3}")

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
        client1 = ClientCodeclass.clientclass(species[i][0], species[j][0]) # Client initializeren
        request = client1.ask() #
        if species[i][0] == species[j][0]:
            toapend.append(1.0)
        else:
            answer = genomediff(species[i][1], species[j][1], client1, f"{species[i][0]}{species[j][0]}", request)
            toapend.append(answer)
        client1.closee()
        newts = datetime.datetime.now()

        print(i + 1, " said ", " i'm done with comparing ", j + 1 + -i, " from ", len(species) - i, " , the time is",
              newts.time())
    return_dict[species[i][0]] = toapend
    print(species[i][0], " ", toapend)
    return return_dict


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
    for i in ronny:
        print("start procces %i" % (i+1))
        p = multiprocessing.Process(target=algorithm, args=(species, i, return_dict))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    with open('result_test.json', 'w') as fp:
        json.dump(return_dict.copy(), fp)
    fp.close()

