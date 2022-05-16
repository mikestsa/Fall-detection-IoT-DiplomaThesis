import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import copy
from tensorflow.keras import models
from tensorflow.keras.models import model_from_json

#from count_falls import count_falls
from gravity_remove import gravity_remove
from list_to_np import list_to_np
from moving_average import moving_average

import redis
import json

from time import sleep
from datetime import datetime


# path = "/home/pi/diploma"
# os.chdir(path)
#model = tf.keras.models.load_model(path)

r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

def redis_to_predict(model,r):

    #df=pd.read_csv("dataraf.txt")
    data_list = []
    data = r.lrange('accel',0,299)
    for i in range(len(data)):
        data_list.append(json.loads(data[i]))

    df = pd.DataFrame (data_list, columns = ['x', 'y', 'z','fall'])
    #print(df)


    windows = df[["x", "y", "z"]]

    #print(windows)
    windows=gravity_remove(windows)
    windows=moving_average(windows,5)

    # for i in range(0, len(df) - 10 * 30,  8* 30):
    #         arxi_parathirou = i
    #         telos_parathirou = i + 30*10
    #         datatemp1 = df[arxi_parathirou:telos_parathirou]
    #         windows.append(datatemp1)
    windows=[windows[:]]
    list=list_to_np(windows)

    #windows=list_to_np(windows)
    list= list.astype('float32')


    predictions=model.predict(list)
    #print(predictions)
    predictions = np.around(predictions)

    #print("oi provlepseis einai")
    with np.printoptions(threshold=0.9):
        dateTimeObj = datetime.now()
        print(dateTimeObj)
        print(predictions)

    r.ltrim('accel',240,-1)


if __name__ == '__main__':

    with open('fashionmnist_model.json', 'r') as json_file:
        json_savedModel= json_file.read()

    #load the model architecture
    model = tf.keras.models.model_from_json(json_savedModel)
    model.load_weights('FashionMNIST_weights.h5')
    #model.summary()

    while 1:
        if (r.llen('accel') > 300 ):
            redis_to_predict(model,r)
        else:
            #print("accel is ")
            #print(r.llen('accel'))
            sleep(0.05)
