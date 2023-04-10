# -*- coding: utf-8 -*-
"""51800969_Pham_Viet_Dung_51900621_Nguyen_Quoc_Dai_So_2_Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OtgroJ8EA5KR3CK005pyrI1QpaV9jP47
"""

import pandas as pd
import numpy as np
from google.colab import drive
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization,AveragePooling2D
from keras.losses import categorical_crossentropy
from tensorflow.keras.optimizers import Adam
from keras.regularizers import l2
from keras.utils import np_utils
from keras.preprocessing import image
from matplotlib import pyplot as plt

drive.mount('/content/drive')
data = pd.read_csv('/content/drive/MyDrive/BigData/fer2013.csv')
data.head()

emotion_map = {0: 'Angry', 1: 'Digust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
emotion_counts = data['emotion'].value_counts(sort=False).reset_index()
emotion_counts.columns = ['emotion', 'number']
emotion_counts['emotion'] = emotion_counts['emotion'].map(emotion_map)
emotion_counts

X_train, train_y, X_test, test_y, X_check, check_y=[],[],[],[],[],[]
for index, row in data.iterrows():
  val=row['pixels'].split(" ")
  if 'Training' in row['Usage']:
    X_train.append(np.array(val,'float32'))
    train_y.append(row['emotion'])
  elif 'PublicTest' in row['Usage']:
    X_test.append(np.array(val,'float32'))
    test_y.append(row['emotion'])
  elif 'PrivateTest' in row['Usage']:
    X_check.append(np.array(val,'float32'))
    check_y.append(row['emotion'])

num_labels = 7
batch_size = 64
epochs = 60
width, height = 48, 48

X_train = np.array(X_train,'float32')
train_y = np.array(train_y,'float32')
X_test = np.array(X_test,'float32')
test_y = np.array(test_y,'float32')
X_check = np.array(X_check,'float32')
check_y = np.array(check_y,'float32')

print(X_train[0])

train_y=np_utils.to_categorical(train_y, num_classes=num_labels)
test_y=np_utils.to_categorical(test_y, num_classes=num_labels)
check_y=np_utils.to_categorical(check_y, num_classes=num_labels)

print(train_y[0])

X_train -= np.mean(X_train, axis=0)
X_train /= np.std(X_train, axis=0)

X_test -= np.mean(X_test, axis=0)
X_test /= np.std(X_test, axis=0)

X_check -= np.mean(X_check, axis=0)
X_check /= np.std(X_check, axis=0)

X_train = X_train.reshape(X_train.shape[0], 48, 48, 1)

X_test = X_test.reshape(X_test.shape[0], 48, 48, 1)

X_check = X_check.reshape(X_check.shape[0], 48, 48, 1)

print(X_train[0])

model = Sequential()

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(X_train.shape[1:])))
model.add(Conv2D(64,kernel_size= (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2), strides=(2, 2)))

model.add(Flatten())

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(num_labels, activation='softmax'))

opt = Adam(learning_rate=0.0001, decay=1e-6)
model.compile(loss = 'categorical_crossentropy', 
              optimizer = opt, 
              metrics = ['accuracy'])

history = model.fit(X_train, train_y,
                    batch_size = batch_size,
                    epochs = epochs,
                    verbose = 1,
                    validation_data = (X_test, test_y),
                    shuffle = True)

module_json = model.to_json()
with open("module.json", "w") as json_file:
  json_file.write(module_json)
model.save_weights("module.h5")

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
epochs = range(len(acc))

plt.plot(epochs, acc, 'b', label='Training Accuracy')
plt.plot(epochs, val_acc, 'r', label='Validation Accuracy')
plt.title('Accuracy Graph')
plt.legend()
plt.figure()

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(len(acc))

plt.plot(epochs, loss, 'b', label='Training Loss')
plt.plot(epochs, val_loss, 'r', label='Validation Loss')
plt.title('Loss Graph')
plt.legend()

plt.show()

y = model.predict(X_check)

y_pred = np.array([np.argmax(i) for i in y])

y_check_class = np.array([np.argmax(i) for i in check_y])
print("Accuracy: ",sum(y_pred==y_check_class)/len(y_pred))

emotion_map = {0: 'Angry', 1: 'Digust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

img = image.load_img("PrivateTest_2134320.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)

img = img.reshape(1,48,48,1)
result = model.predict(img)
result = list(result[0])
img_index = result.index(max(result))
print("Predict: ", emotion_map[img_index])

img = image.load_img("PrivateTest_3447769.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)

img = img.reshape(1,48,48,1)
result = model.predict(img)
result_label = result.argmax()
print("Predict: ", emotion_map[result_label])

img = image.load_img("PrivateTest_3783569.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)

img = img.reshape(1,48,48,1)
result = model.predict(img)
result_label = result.argmax()
print("Predict: ", emotion_map[result_label])

img = image.load_img("PrivateTest_14592510.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)


img = img.reshape(1,48,48,1)
result = model.predict(img)
result_label = result.argmax()
print("Predict: ", emotion_map[result_label])

img = image.load_img("PublicTest_99509833.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)


img = img.reshape(1,48,48,1)
result = model.predict(img)
result_label = result.argmax()
print("Predict: ", emotion_map[result_label])

img = image.load_img("PrivateTest_52177909.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)

img = img.reshape(1,48,48,1)
result = model.predict(img)
result_label = result.argmax()
print("Predict: ", emotion_map[result_label])

img = image.load_img("PrivateTest_4002000.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)

img = img.reshape(1,48,48,1)
result = model.predict(img)
result_label = result.argmax()
print("Predict: ", emotion_map[result_label])

img = image.load_img("PrivateTest_4658147.jpg",target_size = (48,48),color_mode = "grayscale")
img = np.array(img)
plt.imshow(img)
img = np.expand_dims(img,axis = 0)

img = img.reshape(1,48,48,1)
result = model.predict(img)
result_label = result.argmax()
print("Predict: ", emotion_map[result_label])