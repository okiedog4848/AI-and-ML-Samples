"""
This is a sampling of code work as I go through Laurence Moroney book AI-and-ML-for-Coders

My plan is to just add functions for each chapter
"""
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

def chap1_sample():
    l0 = Dense(units=1, input_shape=[1])
    model = Sequential([l0])
    model.compile(optimizer='sgd', loss='mean_squared_error')

    xs = np.array([-1.0, 0.0, 1.0, 2.0, 3.0, 4.0], dtype=float)
    ys = np.array([-3.0, -1.0, 1.0, 3.0, 5.0, 7.0], dtype=float)

    x_input = [10.0]
    x_input_np = np.array(x_input)

    model.fit(xs, ys, epochs=500)

    print(model.predict(x_input_np)) # Had to change to an np array from example
    print("Here is what I learned: {}".format(l0.get_weights()))

if __name__ == "__main__":
    chap1_sample()