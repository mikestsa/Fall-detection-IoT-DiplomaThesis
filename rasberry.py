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

# path = "/home/pi/diploma"
# os.chdir(path)
#model = tf.keras.models.load_model(path)


with open('fashionmnist_model.json', 'r') as json_file:
    json_savedModel= json_file.read()

#load the model architecture
model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('FashionMNIST_weights.h5')
#model.summary()


df=pd.read_csv("dataraf.txt")


df=gravity_remove(df)
df=moving_average(df,5)

windows = []
#df1 = copy.deepcopy(df)
df = df[["x", "y", "z"]]
labels = []


for i in range(0, len(df) - 10 * 30,  8* 30):
        arxi_parathirou = i
        telos_parathirou = i + 30*10
        datatemp1 = df[arxi_parathirou:telos_parathirou]
        windows.append(datatemp1)



windows=list_to_np(windows)
windows= windows.astype('float32')

print(windows)
print(type(windows))
print(len(windows))

predictions=model.predict(windows)
print(predictions)
predictions = np.around(predictions)

print("oi provlepseis einai")
with np.printoptions(threshold=0.9):
    print(predictions)
