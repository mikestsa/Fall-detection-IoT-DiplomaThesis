import pandas as pd
import copy
import math

def gravity_remove(data):

    datatemp= copy.deepcopy(data)
    #:
     #   datatemp.columns = ['x', 'y', 'z', 'fall']

    #x=datatemp['x']
    #y = datatemp['y']
    #z = datatemp['z']
    for i in range(0, len(datatemp)):
        mean2 = datatemp['x'][i]**2+ datatemp['y'][i]**2 + datatemp['z'][i]**2
        mean = math.sqrt(mean2)
        datatemp['x'][i]=datatemp['x'][i]*((mean-1)/mean)
        datatemp['y'][i]=datatemp['y'][i]*((mean-1)/mean)
        datatemp['z'][i]=datatemp['z'][i]*((mean-1)/mean)
    return datatemp
