import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import json
import array

def upp2sym(a):
    return np.where(a,a,a.T)

def sort_by_values_len(dict):
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict


if __name__ == "__main__":
    f = open('final_matrix.json')
    data_json = json.load(f)
    pre_sorted_data = sort_by_values_len(data_json)

    sorted_data = {}
    for i in pre_sorted_data:
        for key, value in i.items():
            sorted_data[key] = value

    names = []
    ut_matrix = []
    for key, value in sorted_data.items():
        names.append(key)
        if len(value) != 29:
            new_list = []
            zero_list = []
            difference = 29 - len(value)
            for zero in range(difference):
                zero_list.append(0)
            new_list = zero_list + value
            sorted_data[key] = new_list
        ut_matrix.append(sorted_data[key])

    test = np.array(ut_matrix)
    matrix = upp2sym(test)

    temp_list = []
    for y in matrix:
        temp_list.append(y.tolist())

    final_matrix = {}
    for key, value in sorted_data.items():
        final_matrix[key] = temp_list[0]
        temp_list.pop(0)

    df = pd.DataFrame(final_matrix, columns=names)

    df.index= names

    #corrMatrix = df.corr()
    # Increase the size of the heatmap.
    plt.figure(figsize=(32, 12))
    # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
    # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
    heatmap = sn.heatmap(df, vmin=0.5, vmax=1, annot=True, fmt=".4f")
    # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize': 12}, pad=12)
    plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

    #len op hoeveelheid da erin staat en dan telkens max