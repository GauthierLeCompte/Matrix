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
        Calculates the levenshtein distance ratio of similarity between two strings
    """
    x = Levenshtein.ratio(s, t)
    return x


def genomediff(x, y, client1, request):
    """
    loop over het grootste genoom en zoek het levenshtein ratio tussen dat 
    deel van het grootste genoom en het kleinste genoom
    :param x: genome 1
    :param y: genome 2
    :param client1: client that handled this
    :param request: None of the json met progress
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
    # zie welk genoom het langste is
    if lenx < leny:
        longest = leny
        swapped = True
        count = leny - lenx
        smallest = lenx
    # als er al progress hervat dan van hier
    if request != None:
        dataname = request
        if dataname["final"] == True:
            return dataname["result"]
        start = dataname["i"]
        final = dataname["result"]
    # als 1 genome volledig is en de andere partial zoek dan rond plaats 14000 
    else:
        if longest > 14000 and smallest <10000:
            start = 14100 - (smallest*2)
            count = min(count, 14200+smallest*2)

    step = 100
    steptotal = 0
    #loop over het grootste genoom
    for i in range(start, count + 1):
        step += 1
        steptotal +=1
        usedx = x[i:leny + i]
        usedy = y
        if swapped:
            usedx = x
            usedy = y[i:lenx + i]
        result = levenshtein_ratio_and_distance(usedx, usedy)
        #als er een nieuw beste resultaat is update en update de server
        if result > final:
            final = result
            client1.update(final, i, False)
            step = 0
            # schrijf progress om de honderd stappen weg naar de server
        if step>=100:
            client1.update(final, i, False)
            step = 0
    #stuur het finale resultaat door naar de server
    client1.update(final, count, True)
    print(f"this were the steps {steptotal}")
    return final


def algorithm(species, i, return_dict):
    """
    go over every collum of the row i
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
            answer = genomediff(species[i][1], species[j][1], client1, request)
            toapend.append(answer)
        client1.closee()
        newts = datetime.datetime.now()

        print(i + 1, " said ", " i'm done with comparing ", j + 1 + -i, " from ", len(species) - i, " , the time is",
              newts.time())
    return_dict[species[i][0]] = toapend
    print(species[i][0], " ", toapend)
    return return_dict


if __name__ == "__main__":
    #lees sequenties in
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
    #per rij start een nieuw proces
    for i in range(0,29):
        print("start procces %i" % (i+1))
        p = multiprocessing.Process(target=algorithm, args=(species, i, return_dict))
        processes.append(p)
        p.start()
    #join de processen 
    for process in processes:
        process.join()
    #schrijf resultaat uit naar een json
    with open('final_matrix.json', 'w') as fp:
        json.dump(return_dict.copy(), fp)
    fp.close()

