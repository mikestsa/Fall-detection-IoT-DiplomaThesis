import pickle as pkl
import pandas as pd
import scipy
import plotly.graph_objects as go
import numpy as np
import os
import os.path
import pyopy
import plotly.graph_objects as go
import matplotlib
import plotly.express as px
import matplotlib.pyplot as plt
from scipy import signal

import plotly.graph_objects as go
import csv

from scipy import signal
from split_by_classes import split_by_classes


from notch import notch
from resample import resample
from smartfall import smartfall
from smartwatch import smartwatch

"""
notch at 31.25 Hz
smartwatch at 31.25 Hz
smartfall at 31.25 Hz
"""


def load_datasets():
    data1 = smartfall()
    # print("smartfall")
    # print(data1)

    data2 = notch()

    # print("notch")
    # print(data2)

    data3 = smartwatch()
    # print("smartwatch")
    # print(data3)

    frames = [data1, data2, data3]

    result = pd.concat([data1, data2,data3], ignore_index=True)




    return result
