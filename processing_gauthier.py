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

def test(species, i, return_dict):
    toapend = []
    for j in range(i, len(species)):
        if species[i][0] == species[j][0]:
            toapend.append(100.0)
        else:
            answer = genomedif(species[i][1], species[j][1])
            toapend.append(answer)

        newts = datetime.datetime.now()

        print(i + 1, " from ", len(species), " and done with comparing ", j + 1, " from ", len(species) - i, " seconds, the time is", newts.time())
    return return_dict


def genomedif(x, y):
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


f = open('sequenties.json', )
data = json.load(f)
species = []
for i in data['species']:
    specie = [i["name"], i["genome"]]
    species.append(specie)
f.close()

x = 1
answerdict = {}
oldts = datetime.datetime.now()
threadcount = 0
# for i in range(1, len(species)):
processes = []
return_dict = multiprocessing.Manager().dict()
for i in range(12, 21):
    print(i)
    p = multiprocessing.Process(target=test, args=(species, i, return_dict))
    processes.append(p)
    p.start()

for process in processes:
    process.join()


# print(return_dict[14])
with open('result_gauthier.json', 'w') as fp:
    json.dump(return_dict.copy(), fp)

# jsonStr = json.dumps(return_dict)

# t12 = multiprocessing.Process(target=test, args=(species, 12))
# t13 = multiprocessing.Process(target=test, args=(species, 13))
# t14 = multiprocessing.Process(target=test, args=(species, 14))
# t15 = multiprocessing.Process(target=test, args=(species, 15))
# t16 = multiprocessing.Process(target=test, args=(species, 16))
# t17 = multiprocessing.Process(target=test, args=(species, 17))
# t18 = multiprocessing.Process(target=test, args=(species, 18))
# t19 = multiprocessing.Process(target=test, args=(species, 19))
# t20 = multiprocessing.Process(target=test, args=(species, 20))
# t12.start()
# t13.start()
# t14.start()
# t15.start()
# t16.start()
# t17.start()
# t18.start()
# t19.start()
# t20.start()


#     for j in range(i, len(species)):
#         if species[i][0] == species[j][0]:
#             if species[i][0] in answerdict:
#                 answerdict[species[i][0]].append("-")
#             else:
#                 answerdict[species[i][0]] = ["-"]
#         else:
#             thread1 = myThread(threadcount, "Thread-%i" % (threadcount), threadcount, species[i][1], species[j][1])
#             answer = thread1.start()
#             if species[i][0] in answerdict:
#                 answerdict[species[i][0]].append(answer)
#             else:
#                 answerdict[species[i][0]] = [answer]
#
#         newts = datetime.datetime.now()
#         compts = newts - oldts
#
#         print(i + 1, " from ", len(species), " and done with comparing ", j + 1, " from ", len(species) - i, " in ",
#               compts.seconds, " seconds,  the time is", newts.time())
#         oldts = datetime.datetime.now()
#
# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # Start new Threads
# thread1.start()
# thread2.start()

