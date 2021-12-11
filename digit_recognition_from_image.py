# -*- coding: utf-8 -*-
"""Digit Recognition from Image.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13gvqyHRxVebQbeZVvWC08iQVQOMr8n63
"""

import numpy 
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist

from tensorflow.python.client import device_lib
device_lib.list_local_devices()

"""Training Dataset: This contains 60,000 data points.
Testing Dataset: This contains 10,000 data points.
"""

(X_train, y_train), (X_test, y_test) = mnist.load_data()

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

"""# Plotting Images in grey scale"""

plt.subplot(221)
plt.imshow(X_train[0], cmap=plt.get_cmap('gray'))
plt.subplot(222)
plt.imshow(X_train[1], cmap=plt.get_cmap('gray'))
plt.subplot(223)
plt.imshow(X_train[2], cmap=plt.get_cmap('gray'))
plt.subplot(224)
plt.imshow(X_train[3], cmap=plt.get_cmap('gray'))
# Show the plot
plt.show()

"""# Formatting Data and Labels for Keras
Now, we will flatten our array of images into a vector of 28×28=784 numbers. As long as we’re consistent between images, it is irrespective of how we flatten the array. From this perspective, the images of the given dataset are just a bunch of points in a 784-dimensional vector space. But the data should always be of the format “(Number of data points, data point dimension)”. In this example, the training data will be of the dimension 60,000×784.
"""

num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')
X_train = X_train / 255 
X_test = X_test / 255
y_train = to_categorical(y_train) 
y_test = to_categorical(y_test)
num_classes = y_test.shape[1]

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

"""# Single layer Neural Network Model
Here we will define a single-layer neural network. It will have an input layer of 784 neurons, i.e. the input dimension and output layer of 10 neurons, i.e. a number of classes. The activation function used will be softmax activation.
"""

# create model
model = Sequential()  
model.add(Dense(num_classes, input_dim=num_pixels, activation='softmax'))

"""# Compiling the Model
Once we defined our first model, our next step is to compile it. While compiling we have to give the loss function to be used, the optimizer, and any metric as an input. Here we will use

Cross-entropy loss as a loss function,
SGD as an optimizer, and
Accuracy as a metric.
"""

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

"""# Training or Fitting the Model
After compilation, our model is ready to be trained. Now, we will provide training data to the neural network. Also, we have to specify the validation data, over which the model will only be validated along with the number of epochs and batch size as hyperparameter
"""

# Training model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)

"""# Evaluating the Model"""

# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

"""# Multi-Layer Neural Network Model
Now we will define a multi-layer neural network in which we will add 2 hidden layers having 500 and 100 neurons.
"""

model = Sequential()
model.add(Dense(500, input_dim=num_pixels, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

"""# Compiling the Model
Once we defined our second model, our next step is to compile it. While compiling we have to give the loss function to be used, the optimizer, and any metric as an input. Here we will use

Cross-entropy loss as a loss function,
Adam optimizer as an optimizer, and
Accuracy as a metric.
"""

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

"""# Deep Neural Network Model
Now we will define a deep neural network in which we will add 3 hidden layers having 500, 100 and 50 neurons respectively
"""

model = Sequential()  
model.add(Dense(500, input_dim=num_pixels, activation='sigmoid'))
model.add(Dense(100, activation='sigmoid'))
model.add(Dense(50, activation = 'sigmoid'))
model.add(Dense(num_classes, activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)

# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

"""# Analyzing Model Summary"""

model.summary()

"""# Save the Model
The phrase "Saving a TensorFlow model" typically means one of two things:

Checkpoints, OR
SavedModel.
Checkpoints capture the exact value of all parameters (tf.Variable objects) used by a model. Checkpoints do not contain any description of the computation defined by the model and thus are typically only useful when source code that will use the saved parameter values is available.

The SavedModel format on the other hand includes a serialized description of the computation defined by the model in addition to the parameter values (checkpoint). Models in this format are independent of the source code that created the model. They are thus suitable for deployment via TensorFlow Serving, TensorFlow Lite, TensorFlow.js, or programs in other programming languages (the C, C++, Java, Go, Rust, C# etc. TensorFlow APIs)
"""

import h5py
# Compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Training model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)
model.save_weights('FC.h5')
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

"""# Loading the saved Model
Now, we will load the model which we have just saved and compare that with the random model. Here firstly we have created a random model and then load the previously saved model and compare the error of both.
"""

model = Sequential()
model.add(Dense(500, input_dim=num_pixels, activation='sigmoid'))
model.add(Dense(100, activation='sigmoid'))
model.add(Dense(50, activation = 'sigmoid'))
model.add(Dense(num_classes, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

model.load_weights('FC.h5')
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

"""# Creating checkpoints of Model
Here we make the model checkpoints (i.e, point after that there is no significant reduction in the validation error) and saved the weights of that point and used further wherever required.
"""

from tensorflow.keras.callbacks import ModelCheckpoint
filepath='FC.h5'
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', save_best_only=True, mode='max')
callbacks_list = [checkpoint]
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, callbacks=callbacks_list)

"""# Defining Learning Rate Decay and Other Parameters of Optimizer
We will use the SGD and Adam Optimizer for our model. 
"""

from tensorflow.keras.optimizers import SGD, Adam
sgd = SGD(lr = 0.001, momentum = 0.0005, decay = 0.0005)   # 0.001  to 0.000001
adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0005)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
# model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

"""# Defining Regularizers for the Model"""

from tensorflow.keras import regularizers
from tensorflow.keras.layers import Dropout
model = Sequential() 
model.add(Dense(500, input_dim=num_pixels, activation='sigmoid', kernel_regularizer=regularizers.l2(1e-4)))
model.add(Dropout(0.3))
model.add(Dense(100, activation='sigmoid', kernel_regularizer=regularizers.l2(1e-4)))
model.add(Dropout(0.25))
model.add(Dense(50, activation = 'sigmoid', kernel_regularizer=regularizers.l2(1e-4)))
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation='softmax', kernel_regularizer=regularizers.l2(1e-4)))
# Compile model
from tensorflow.keras.callbacks import ModelCheckpoint
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Training model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))

"""# Defining Initialization for the Model
Add dropout regularization and glorot weight initialization technique in the model
"""

from tensorflow.keras import initializers
from tensorflow.keras.layers import Dropout
model = Sequential()
model.add(Dense(500, input_dim=num_pixels, activation='sigmoid', kernel_initializer=initializers.GlorotNormal()))
model.add(Dense(100, activation='sigmoid', kernel_initializer=initializers.GlorotNormal()))
model.add(Dense(50, activation = 'sigmoid', kernel_initializer=initializers.GlorotNormal()))
model.add(Dense(num_classes, activation='softmax', kernel_initializer=initializers.GlorotNormal()))
# Compile model
from tensorflow.keras.callbacks import ModelCheckpoint
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Training model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))