#https://github.com/kashif/tf-keras-tutorial/blob/tf2/1-fashion-mnist-with-keras.ipynb
'''
Mateusz Miekicki s20691
Oskar Przydatek s19388
Identifying clothes using a database from Zalando.
'''
import tensorflow as tf
import numpy as np
'''
Downloading the data set and dividing it into test and learning data.
'''
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.fashion_mnist.load_data()
import random
import matplotlib.pyplot as plt

i = random.randint(0, 100)

print("Label: %s" % train_labels[i])
plt.imshow(train_images[i], cmap='gray')
plt.draw()
TRAINING_SIZE = len(train_images)
TEST_SIZE = len(test_images)

'''
Reshape from (N, 28, 28) to (N, 28*28=784)
'''
train_images = np.reshape(train_images, (TRAINING_SIZE, 784))
test_images = np.reshape(test_images, (TEST_SIZE, 784))

'''
Convert the array to float32 as opposed to uint8
'''
train_images = train_images.astype(np.float32)
test_images = test_images.astype(np.float32)

'''
Convert the pixel values from integers between 0 and 255 to floats between 0 and 1
'''
train_images /= 255
test_images /=  255

NUM_CAT = 10

'''
The format of the labels before conversion
'''
print("Before", train_labels[0])  

train_labels  = tf.keras.utils.to_categorical(train_labels, NUM_CAT)
'''
The format of the labels after conversion
'''
print("After", train_labels[0])  

test_labels = tf.keras.utils.to_categorical(test_labels, NUM_CAT)

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(512, activation=tf.nn.relu, input_shape=(784,)))
model.add(tf.keras.layers.Dense(NUM_CAT, activation=tf.nn.softmax))

'''
compile and print out a summary of our model
'''
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=5)
loss, accuracy = model.evaluate(test_images, test_labels)
print('Test accuracy: %.2f' % (accuracy))