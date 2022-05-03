
import pandas as pd
import os
import os.path



def notch():
    path = 'C:\\python\\FallDetection\\dataset\\notch'
    os.chdir(path)
    filepath = "C:\python\FallDetection\dataset/notch"


    # Reading data from file1
    with open('32ms_User1_LeftWrist.csv') as fp:
        data1 = fp.read()

    # Reading data from file2
    with open('32ms_User2_LeftWrist.csv') as fp:
        data2 = fp.read()

    # Reading data from file3
    with open('32ms_User3_LeftWrist.csv') as fp:
        data3 = fp.read()

    # Reading data from file4
    with open('32ms_User4_LeftWrist.csv') as fp:
        data4 = fp.read()

    # Reading data from file5
    with open('32ms_User5_LeftWrist.csv') as fp:
        data5 = fp.read()

    # Reading data from file6
    with open('32ms_User6_LeftWrist.csv') as fp:
        data6 = fp.read()

    # Reading data from file7
    with open('32ms_User7_LeftWrist.csv') as fp:
        data7 = fp.read()

    # Merging all files
    # To add the data of file2
    # from next line
    data = data1
    data += "\n"
    data += data2
    data += "\n"
    data += data3
    data += "\n"
    data += data4
    data += "\n"
    data += data5
    data += "\n"
    data += data6
    data += "\n"
    data += data7

    with open('all.csv', 'w') as fp:
        fp.write(data)

    df = pd.read_csv("all.csv")
    df = df[["Acc_x [m/s^2]", "Acc_y [m/s^2]", "Acc_z [m/s^2]", "AnyFall"]]
    df.columns = ['x', 'y', 'z', 'fall']

    df["x"] = 0.102 * df["x"]#m/s^2 to g*m/s^2
    df["y"] = 0.102 * df["y"]
    df["z"] = 0.102 * df["z"]


    return df
