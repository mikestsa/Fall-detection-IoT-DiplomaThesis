import numpy as np


def list_to_np(list):

    array = np.zeros((len(list), 300,3))

    for i in range(0,len(list)):
        array[i] = list[i]
    return array
