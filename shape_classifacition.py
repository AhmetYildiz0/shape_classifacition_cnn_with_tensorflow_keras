# -*- coding: utf-8 -*-
"""Shape_Classifacition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AFKmaA0zX5CV37S2NiDhaOpANhq_M9uY
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount("/content/drive/")

import os
os.chdir("/content/drive/MyDrive/yapay_zeka_video/S-005-Shape-Classifacition")

from tqdm import tqdm
import cv2
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.layers import *

# dataset from https://www.kaggle.com/cactus3/basicshapes
# get the dataset

data_x,data_y=[],[]
img_size=28
data_main_path="shapes/"
labels=os.listdir(data_main_path)


for label in labels:
  file_path=os.listdir(data_main_path+label+"/")
  print(label+" :")
  for path in tqdm(file_path):
    img=cv2.imread(data_main_path+label+"/"+path)
    img=cv2.resize(img, (img_size,img_size), interpolation = cv2.INTER_AREA)
    data_x.append(img)
    data_y.append([1 if x==labels.index(label) else 0 for x in range(len(labels))])

  
data_x,data_y=np.array(data_x),np.array(data_y)

choice=np.random.choice(np.arange(0,len(data_x)),(30,))

plt.figure(figsize=(19,7))

for x in range(len(choice)):
  plt.subplot(4,9,x+1)
  plt.imshow(data_x[choice[x]],cmap='gray')

plt.tight_layout()
plt.show()

del choice

x_train, x_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.33,random_state=42)

del data_x,data_y

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
  rotation_range=20,
  zoom_range=0.2,
  shear_range=0.2,
  width_shift_range=0.2,
  height_shift_range=0.2,
  horizontal_flip=True,
  vertical_flip=True,
  rescale=1./255)

train_datagen.fit(x_train,seed=42)

test_datagen=tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
test_datagen.fit(x_test,seed=42)

print("x_train :",x_train.shape)
print("y_train :",y_train.shape)
print("x_test  :",x_test.shape)
print("y_test  :",y_test.shape)

dropout=0.5
tf.keras.backend.clear_session()

model=tf.keras.models.Sequential()
model.add(InputLayer(input_shape=(img_size,img_size,3)))

model.add(Conv2D(32,(3,3)))
model.add(Conv2D(32,(3,3)))
# model.add(LeakyReLU())
model.add(MaxPool2D((2,2)))

model.add(Conv2D(64,(3,3)))
model.add(Conv2D(64,(3,3)))
# model.add(LeakyReLU())
model.add(MaxPool2D((2,2)))

# model.add(BatchNormalization())
model.add(Dropout(dropout))
model.add(Flatten())

model.add(Dense(256))
model.add(Dropout(dropout))
model.add(LeakyReLU())
model.add(Dense(256))
model.add(Dropout(dropout))
model.add(LeakyReLU())
model.add(Dense(len(labels),activation='softmax'))

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
model.summary()

history=model.fit(train_datagen.flow(x_train, y_train, batch_size=32), 
                    epochs=200,
                    steps_per_epoch=x_train.shape[0]//32, # number of images comprising of one epoch
                    validation_data=test_datagen.flow(x_test, y_test), # data for validation
                    validation_steps=x_test.shape[0]//32)

plt.figure(figsize=(19,7))
plt.subplot(1,2,1)
plt.plot(history.history['loss'],'b-')
plt.plot(history.history['val_loss'],'r-')
plt.legend(['loss','val_loss'])
plt.title('Loss')

plt.subplot(1,2,2)
plt.plot(history.history['accuracy'],'b-')
plt.plot(history.history['val_accuracy'],'r-')
plt.legend(['accuracy','val_accuracy'])
plt.title('Accuracy')

plt.tight_layout()
plt.show()

# evaluate the model
result_train_data=model.evaluate(test_datagen.flow(x_train, y_train),verbose=0)
result_test_data=model.evaluate(test_datagen.flow(x_test,y_test),verbose=0)

print("<======Result=======>")
print("Trian Loss     : ",round(result_train_data[0],ndigits=3))
print("Trian Accuracy :%",round(result_train_data[1],ndigits=3)*100)
print()
print("Test  Loss     : ",round(result_test_data[0],ndigits=3))
print("Test  Accuracy :%",round(result_test_data[1],ndigits=3)*100)

# save the model
model.save("Shape_Classifacition.h5")