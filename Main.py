import json

f = open('sequenties.json', )

data = json.load(f)
species = [[]]
for i in data['species']:
    specie = [i["name"], i["genome"]]
    species.append(specie)
f.close()

for i in species:
    for j in species:
        if i == j:
            break