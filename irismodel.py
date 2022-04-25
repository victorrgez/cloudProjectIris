#!/usr/bin/env python
# coding: utf-8

from tensorflow import keras
import numpy as np


class IrisModel:
    """Returns a trained model for Iris Flowers Classification"""

    def __init__(self):
        """ Loads the model and creates Dictionaries to interpret the predictions"""
        self.varietiesToNumbers = {"Versicolor": 0, "Setosa": 1, "Virginica": 2}
        self.numbersToVarieties = {}
        for key, value in self.varietiesToNumbers.items():
            self.numbersToVarieties[value] = key
        self.model = keras.models.load_model("src/iris.h5")

    def makePrediction(self, features):
        """
        Output (predictedFlower as String, confidence as Float):
         -0 --> Versicolor
         -1 --> Setosa
         -2 --> Virginica

        Input (list of Floats):
         [SepalLength, SepalWidth, PetalLength, PetalWidth)
        """
        predictions = self.model.predict([features])
        predictedFlower = self.numbersToVarieties[np.argmax(predictions)]
        confidence = np.max(predictions) * 100
        return (predictedFlower, confidence)
