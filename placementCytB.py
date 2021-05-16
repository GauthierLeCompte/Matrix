import numpy as np
import json
import datetime

# volgende functie komt van https://www.datacamp.com/community/tutorials/fuzzy-string-python
def levenshtein_ratio_and_distance(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in np.arange(1, rows):
        distance[i][0] = i

    for k in np.arange(1,cols):
        distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return distance[row][col]

#TODO: Uitleg functie
def genomedif(x, y):
    lenx = len(x)
    leny = len(y)
    swapped = False

    count = lenx-leny
    if lenx<leny:
        swapped = True
        count = leny-lenx

    besti = 0
    final = 0
    for i in range(count+1):
        usedx = x[i:leny+i]
        usedy = y
        if swapped:
            usedx = x
            usedy = y[i:leny + i]

        result2 = levenshtein_ratio_and_distance(usedx, usedy, True)
        if result2 > final:
            besti = i
            final = result2
    print("BESTE I: ", besti)
    return final


def getGenome(name):
    '''
    Returns the sequence for the specified name
    :param name: the specified name
    :return: genome sequence
    '''
    for i in range(len(species)):
        if species[i][0] == name:
            return species[i][1]
    return None

f = open('sequenties.json', )
data = json.load(f)
species = []
for i in data['species']:
    specie = [i["name"], i["genome"]]
    species.append(specie)
f.close()

answerdict = {}
oldts = datetime.datetime.now()

comparison_dict = {"Ailurus_fulgens": "Canis_rufus",
                   "Vulpes_vulpes": "Canis_lupus_pallipes",
                   "Canis_latrans": "Canis_simensis",
                   "Canis_lupus_chanco": "Lycalopex_culpaeus",
                   "Canis_lupus_familiaris": "Lycalopex_vetulus",
                   "Canis_lupus_lupus": "Lycalopex_griseus"}

for key, value in comparison_dict.items():
    answer = genomedif(getGenome(key), getGenome(value))
    if key in answerdict:
        answerdict[key].append(answer)
    else:
        answerdict[key] = [answer]

    newts = datetime.datetime.now()
    compts = newts - oldts

    oldts = datetime.datetime.now()
