import numpy as np
from scipy.spatial.transform import Rotation as R
import os
import pandas as pd
import random


def data_augmentation(df,axis):
    dfcopy = df.copy()

    dfx = dfcopy["x"]
    dfy = dfcopy["y"]
    dfz = dfcopy["z"]
    degreesl=list()
    a = np.array([random.randint(30, 120), random.randint(-120,-30)])
    ep=random.randint(0,1)
    degrees=a[ep]




    for i in range(min(df.index),max(df.index)):

        vector = [dfcopy["x"][i], dfcopy["y"][i], dfcopy["z"][i]]
        rotation_radians = np.radians(degrees)
        rotation_axis = np.array(axis)
        rotation_vector = rotation_radians * rotation_axis
        rotation = R.from_rotvec(rotation_vector)
        rotated_vec = rotation.apply(vector)

        dfcopy["x"][i] = rotated_vec[0]
        dfcopy["y"][i]= rotated_vec[1]
        dfcopy["z"][i] = rotated_vec[2]
   # print(degrees)




    return dfcopy
