import pandas as pd
import os
import os.path

from gravity_remove import gravity_remove


def smartfall():
    path = 'C:\python\FallDetection\dataset\smartfall'
    os.chdir(path)
    notch = "/notch"
    smartfall = "/smartfall"
    smartwatch = "/smartwatch"

    filepath = "C:\python\FallDetection\dataset\smartfall"
    with open('SmartFallTesting.csv') as fp:
        data1 = fp.read()

    # Reading data from file2
    with open('SmartFallTraining.csv') as fp:
        data2 = fp.read()


    data = data1
    data += "\n"
    data += data2

    with open('all.csv', 'w') as fp:
        fp.write(data)

    df = pd.read_csv("all.csv")

    df.columns = ['x', 'y', 'z', 'fall']


    df=gravity_remove(df) ##return data without gravity
    return df
