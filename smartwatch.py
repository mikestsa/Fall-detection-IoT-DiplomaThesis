
import os.path
import pandas as pd
import os
import os.path

from gravity_remove import gravity_remove



def smartwatch():
    path = "C:\python\FallDetection\dataset\smartwatch"
    os.chdir(path)



    data = data1 = data2 = data3 = ""




    # Reading data from file2
    with open('raw91_Testing_Relabeled_Auto_25.csv') as fp:
        data2 = fp.read()


    data += data2
    #data += "\n"
    #data += data3

    with open('all.csv', 'w') as fp:
        fp.write(data)
    df = pd.read_csv("all.csv")
    df = df[["x", "y", "z", "outcome"]]
    df.columns = ['x', 'y', 'z', 'fall']


    df = gravity_remove(df)  #return data without gravity
    return df
