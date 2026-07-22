import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print("TensorFlow:", tf.__version__)
print("Keras imported successfully!")


# relu method
modelRelu = keras.Sequential([
    # inpute layer it's contain the input
    layers.Input(shape=(4,)), 
    # hidden layer it perform calculation and learn pattern
    layers.Dense(8, activation="relu"),
    # output layer it gives the final prediction
    layers.Dense(1, activation="sigmoid")
])
modelRelu.summary()

# sigmoid method
modelSigmoid = keras.Sequential([
    layers.Input(shape=(4,)),
    layers.Dense(8, activation="sigmoid"),
    layers.Dense(1, activation="sigmoid")
])

modelSigmoid.summary()

# tanh method
modelTanh = keras.Sequential([
    layers.Input(shape=(4,)),
    layers.Dense(8, activation="tanh"),
    layers.Dense(1, activation="sigmoid")
])

modelTanh.summary()


 
