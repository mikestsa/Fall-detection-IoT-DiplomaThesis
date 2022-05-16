
import copy
def moving_average(data,n):
    datatemp= copy.deepcopy(data)
    datatemp['x']=datatemp['x'].rolling(window=n,min_periods=1).mean()
    datatemp['y']=datatemp['y'].rolling(window=n,min_periods=1).mean()
    datatemp['z']=datatemp['z'].rolling(window=n,min_periods=1).mean()
    return datatemp
