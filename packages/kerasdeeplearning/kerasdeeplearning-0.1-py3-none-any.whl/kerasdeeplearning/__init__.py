def add_number(a,b):
    return a+b

#---------------FFNN FOR SPAM HAM-----------

'''
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.feature_extraction.text import CountVectorizer

data = pd.read_csv('spam_ham_dataset.csv')

X = data['text'].values
y = data['label'].values

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X)
X = X.toarray()
label = LabelEncoder()
y = label.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=42)

model = Sequential()
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.SGD(learning_rate=0.1), metrics=['accuracy'])

hist = model.fit(X_train, y_train , epochs=15)

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss:.4f}')
print(f'Test Accuracy: {accuracy:.4f}')

prediction = model.predict(X)
y_pred = label.inverse_transform(np.round(prediction).astype(int))

data["predicted_text"] = y_pred

spam = data[data["predicted_text"] == "spam"][["label", "text"]]
ham = data[data["predicted_text"] == "ham"][["label", "text"]]
spam.to_csv("spams.csv",index=False)
ham.to_csv("hams.csv",index=False)
'''

#-----------YOLO---------------

'''
!pip install ultralytics
!yolo task = detect mode = predict model = yolov8m.pt source = "dogvideo.mp4"
'''

#--------Spleeter----------------

'''
!pip install spleeter

import os
import shutil
from spleeter.separator import Separator

audio = '/content/song.wav'
output = '/content/latestoutput'

separator = Separator('spleeter:2stems')

separator.separate_to_file(audio, output)

vocals = os.path.join(output)
music = os.path.join(output)
'''

#---------SGD With Nesterov Momentum----------------
'''
import numpy as np

# loss function and its gradient
def loss_function(x):
    return x ** 2

def gradient(x):
    return 2 * x

learning_rate = 0.1
momentum = 0.9
num_epochs = 100
batch_size = 32

x = np.random.rand(1)
v = np.zeros_like(x)

for epoch in range(num_epochs):
    # random batch of data
    batch_data = np.random.rand(batch_size)

    # Computing the gradient
    grad = np.mean(gradient(batch_data))
    # adding velocity with momentum
    v = momentum * v + learning_rate * grad
    # adding parameters with Nesterov Momentum
    x -= v
    loss = np.mean(loss_function(batch_data))
    print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {loss:.4f}")

print(f"Optimal Solution: x = {x[0]:.4f}")
'''

#------------NLP Application-----------
'''
import speech_recognition as sr
import os
import nltk

nltk.download("punkt")

word_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Word.lnk"
googlechrome_path = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Google Chrome.lnk"
#audio_file = "Recording.wav"

recognizer = sr.Recognizer()

# with sr.AudioFile(audio_file) as source:
#     audio_data = recognizer.record(source)
#     raw_text = recognizer.recognize_google(audio_data)

text = "open word"
print("Text from audio:", text)

tokens = nltk.word_tokenize(text)
print("Tokens = ",tokens)

if "open" in tokens:
    if "word" in tokens:
        print("Successfully Opened Word")
        os.startfile(word_path)
    elif "google" in tokens and "chrome" in tokens:
        print("Successfully opened chrome")
        os.startfile(googlechrome_path)
    else:
        print("Unknown command")
else:
    print("No verbs found")
'''

#------------ESN-----------
'''
import numpy as np
import matplotlib.pyplot as plt

#ESN parameters
input_size = 1
reservoir_size = 100
output_size = 1
spectral_radius = 0.9

#random weights for reservoir layer
input_weights = np.random.rand(reservoir_size, input_size)
reservoir_weights = np.random.rand(reservoir_size, reservoir_size) - 0.5
output_weights = np.random.rand(output_size, reservoir_size)

#random initial state for reservoir
reservoir_state = np.random.rand(reservoir_size, 1)

# time series a sine wave
time_steps = 200
time_series = np.sin(np.linspace(0, 4 * np.pi, time_steps))

predicted_values = []

# time series
for t in range(time_steps):
    # Input time t
    current_input = time_series[t]

    # to Update reservoir state
    reservoir_state = np.tanh(
        np.dot(reservoir_weights, reservoir_state) + np.dot(input_weights, current_input)
    )

    # Predict the output at time t+1
    predicted_output = np.dot(output_weights, reservoir_state)

    predicted_values.append(predicted_output[0, 0])

plt.figure(figsize=(10, 5))
plt.plot(time_series, label='True Signal', color='b')
plt.plot(range(1, time_steps), predicted_values[:-1], label='Predicted Signal', color='r')
plt.legend()
plt.title('ESN Time-Series Prediction')
plt.xlabel('Time Step')
plt.ylabel('Value')
plt.show()
'''

#---------------------ICA----------------
'''
#pip install scikit-learn
import numpy as np
from sklearn.decomposition import FastICA
import matplotlib.pyplot as plt

np.random.seed(0)
n_samples = 2000
time = np.linspace(0, 8, n_samples)
s1 = np.sin(2 * time)
s2 = np.sign(np.sin(3 * time))
s3 = np.random.rand(n_samples)

S = np.c_[s1, s2, s3]
A = np.array([[1, 1, 1], [0.5, 2, 1.0], [1.5, 1.0, 2.0]])
X = S.dot(A.T)

ica = FastICA(n_components=3)
S_estimated = ica.fit_transform(X)

plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.title('Original Sources')
plt.plot(S)

plt.subplot(3, 1, 2)
plt.title('Mixed Signals')
plt.plot(X)

plt.subplot(3, 1, 3)
plt.title('Recovered Sources (ICA)')
plt.plot(S_estimated)

plt.tight_layout()
plt.show()
'''

#---------------CIFAR10 DATASET-------------------
'''
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10)  # Output layer for 10 classes
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.2)
model.save("my_cifar10_model.h5")

import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
# Load the saved model
model = tf.keras.models.load_model("my_cifar10_model.h5")

image_path = 'ship.jpg'
img = image.load_img(image_path, target_size=(32, 32))
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

result = model.predict(img_array, verbose=0)

labels = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

max_prob = np.argmax(result)
result = labels[max_prob]

print(f"Predicted Class: {result}")
'''