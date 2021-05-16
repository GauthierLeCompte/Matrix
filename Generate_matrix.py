import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import json
import array

def upp2sym(a):
    '''
    Translates upper traing. matrix into symmetric matrx
    :param a: numpy matrix
    :return: numpy symmetric matrix
    '''
    return np.where(a,a,a.T)

def sort_by_values_len(dict):
    '''
    Sorts the values of a dictionary by length
    :param dict: the dictianory we want to sort
    :return: sorted dictionary
    '''
    dict_len= {key: len(value) for key, value in dict.items()}
    import operator
    sorted_key_list = sorted(dict_len.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = [{item[0]: dict[item [0]]} for item in sorted_key_list]
    return sorted_dict


if __name__ == "__main__":
    # Load in data from json file
    f = open('final_matrix.json')
    data_json = json.load(f)
    pre_sorted_data = sort_by_values_len(data_json)

    # Set corrrect values for sorted data dictionary
    sorted_data = {}
    for i in pre_sorted_data:
        for key, value in i.items():
            sorted_data[key] = value

    names = []
    ut_matrix = []

    # Adds zero's where needed because we have an upper triang. matrix
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

    # Make symmetric matrix
    test = np.array(ut_matrix)
    matrix = upp2sym(test)

    # Change numpy array into dictionary
    temp_list = []
    for y in matrix:
        temp_list.append(y.tolist())

    # Change numpy array into dictionary
    final_matrix = {}
    for key, value in sorted_data.items():
        final_matrix[key] = temp_list[0]
        temp_list.pop(0)

    # Create Dataframe
    df = pd.DataFrame(final_matrix, columns=names)
    df.index= names

    # Increase the size of the heatmap.
    plt.figure(figsize=(32, 12))
    # Store heatmap object in a variable to easily access it when you want to include more features (such as title).
    # Set the range of values to be displayed on the colormap from -1 to 1, and set the annotation to True to display the correlation values on the heatmap.
    heatmap = sn.heatmap(df, vmin=0.5, vmax=1, annot=True, fmt=".4f")
    # Give a title to the heatmap. Pad defines the distance of the title from the top of the heatmap.
    heatmap.set_title('Correlation Heatmap', fontdict={'fontsize': 12}, pad=12)
    plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()