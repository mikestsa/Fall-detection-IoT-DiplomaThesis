import pandas as pd
import os
import matplotlib.pyplot as plt

from count_falls import count_falls
from list_to_np import list_to_np
import copy


def create_windows_labels():
    import copy
    path = "C:\python\FallDetection\dataset\smartwatch"
    os.chdir(path)
    df=load_datasets()
    #df = pd.read_pickle("allDATA.pkl")
    #print((df))
    df1 = copy.deepcopy(df)
    df1=df1[["x","y","z"]]

    windows = []
    labels = []

    import copy

    from data_augmentation import data_augmentation

    import numpy as np

    from dataframe_to_numpy import dataframe_to_numpy

    x, array = count_falls(df)
    print(array)

    for i in range(0, len(df) - 10 * 30,  8* 30):
        arxi_parathirou = i
        telos_parathirou = i + 30*10
        datatemp1 = df1[arxi_parathirou:telos_parathirou]
        windows.append(datatemp1)
        array.append(10000000000)
        for j in range(len(array)):
            if (array[j] > arxi_parathirou + 30) and (array[j] < telos_parathirou - 30):
                labels.append(float(1))  ###uparxei ptwsi
                break
            if array[j] > telos_parathirou:
                labels.append(float(0))  ###den uparxei ptwsi
                break

    for i in range(len(labels)) :
        labels[i]

    print(labels)
    print(len(labels))
    print(len(windows))
    print(len((df)))
    ptwseis = 0
    mh_ptwseis = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            ptwseis = ptwseis + 1
        else:
            mh_ptwseis = mh_ptwseis + 1
        # y.append(float(1))

    print(ptwseis)
    print(mh_ptwseis)




    ####################

    for i in range(0, len(df) - 10 * 30,  8* 30):
        arxi_parathirou = i+150
        telos_parathirou = i + 30*10 +150
        datatemp1 = df1[arxi_parathirou:telos_parathirou]
        windows.append(datatemp1)
        array.append(10000000000)
        for j in range(len(array)):
            if (array[j] > arxi_parathirou + 30) and (array[j] < telos_parathirou - 30):
                labels.append(float(1))  ###uparxei ptwsi
                break
            if array[j] > telos_parathirou:
                labels.append(float(0))  ###den uparxei ptwsi
                break




    ###############
    windows=list_to_np(windows)
    array = np.zeros((2*1182))
    for i in range(len(array)):
        array[i]=labels[i]
    labels=array
    return windows,labels

