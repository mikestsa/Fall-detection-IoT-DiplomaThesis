
from keras.utils import np_utils

from testfi import testfi

import numpy as np
import os
"""
notch at 31.25 Hz without gravity and y axis in m/s^2,106 falls
smartwatch at 31.25 Hz with gravity and y axis in g, (raw data, no fallings), 91(rawtesting), 182(rawtraining) falls
smartfall at 31.25 Hz with gravity and y axis in g,508 falls
"""
path = "C:\python\FallDetection\dataset\smartwatch"
os.chdir(path)
file=np.load("file.npy")


array = np.zeros((2896))



print(array)
for i in range(0,len(array)):
    if i<1448:
        array[i]=float(1.00)
    else:
        array[i]=float(0.00)



from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, Conv1D, MaxPooling1D , Reshape


from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import  Flatten, Dense
print(" x train shape")
print(file.shape)
print(file.shape[0]," training samples")


print(" y train shape")
print(array.shape)
file = file.astype('float32')
array = array.astype('float32')
array = np_utils.to_categorical(array, 2)
time_periods=200
channels=3
file,array=testfi()

print(file.shape)
print(array.shape)
print(array)
print(file)
file = file.astype('float32')
array = array.astype('float32')
array = np_utils.to_categorical(array, 2)

file=file[1:len(file)]
array=array[1:len(array)]
np.save('windows_of_samples_22102021.npy', file)
np.save('labels_of_samples_22102021.npy', array)

##################################
file=np.load("finalwindows610.npy")

array=np.load("finallabels.npy")
file = file.astype('float32')
array = array.astype('float32')
array = np_utils.to_categorical(array, 2)
#######################testttt7/10/5:56
file=np.load("finalwindows22train.npy")
array=np.load("finallabelstrain22.npy")
file = file.astype('float32')
array = array.astype('float32')
array = np_utils.to_categorical(array, 2)

fileval=np.load("finalwindows22val.npy")
arrayval=np.load("finallabels22val.npy")
fileval = fileval.astype('float32')
arrayval = arrayval.astype('float32')
arrayval = np_utils.to_categorical(arrayval, 2)

filetest=np.load("finalwindows22test.npy")
arraytest=np.load("finallabels22test.npy")
filetest= filetest.astype('float32')
arraytest = arraytest.astype('float32')
arraytest= np_utils.to_categorical(arraytest, 2)




################################

model = Sequential()
model.add(Conv1D(filters=32, kernel_size=4, input_shape=file[1].shape,strides=1,activation='relu'))

model.add(MaxPooling1D(15))
model.add(Conv1D(filters=32, kernel_size=1, strides=1,activation='relu'))

model.add(Conv1D(filters=16, kernel_size=4,strides=1,activation='relu'))
model.add(MaxPooling1D(3))
model.add(Dropout(0.25))




model.add(Flatten())

model.add(Dense(16))

model.add(Dense(8))

model.add(Dense(2,activation='softmax'))


model.summary()


opt = Adam(learning_rate=0.001)

model.compile(loss='categorical_crossentropy',optimizer=opt, metrics=['accuracy'])

print(file.shape)
array=array
print(array.shape)

# Hyper-parameters

print(len(array))
print(len(arrayval))
print(len(arraytest))
model.fit(file, array,validation_data=(fileval,arrayval) ,batch_size=32, epochs=50)

model.save(path)




predictions=model.predict(filetest)
predictions = np.around(predictions)
with np.printoptions(threshold=0.9):
    print(predictions)


count=0
for i in range(len(filetest)):
    if arraytest[i][1]==predictions[i][1]:
        count=count+1
acc=count/len(filetest)
print(acc)


###confusion matrix
TP=TN=FP=FN=0
for i in range(len(filetest)):
    if arraytest[i][1]==predictions[i][1]==1:
        TP=TP+1
    if arraytest[i][1] == predictions[i][1] == 0:
        TN = TN + 1
    if arraytest[i][1]==0:
        if predictions[i][1]==1:
          FP=FP+1
    if arraytest[i][1] == 1:
        if predictions[i][1] == 0:
          FN = FN + 1
Precision= TP/(TP+FP)
Recall = TP/(TP+FN)
F1 = 2*(Recall * Precision) / (Recall + Precision)
acc=count/len(filetest)
