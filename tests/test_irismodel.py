from requests import get, post
from time import sleep
from src.irismodel3000.main import parse
from src.irismodel3000.irismodel import IrisModel
import pytest
import json

"""
Make sure we install the requirements on "src/irismodel3000/requirements.txt"
for carrying out these tests since we will need Tensorflow
(not installing TF before in order not to slow down the rest of the tests)
"""


def test_iris_model_is_reachable(normalModel):
    """
    Makes sure that the standard version of the Iris model without monkeypatching
    can be brought up succesfully and that it is reachable through a GET request
    in the health-check endpoint
    """
    sleep(0.1)
    renderedHtml = get("http://localhost:3000").text
    assert "<html><body>Model IS UP AND RUNNING</body></html>" == renderedHtml


@pytest.mark.parametrize("sepalLength,sepalWidth,petalLength,petalWidth,validData", [
    (1.0, 1.0, 1.0, 0.0, False),
    (None, None, None, None, False),
    (-0.1, 2.2, 0.3, 3.5, False),
    (3.2, None, -1, 0.4, False),
    (1.0, None, 1.0, 0.5, False),
    (0.03, 3.1, 1.2, 0.7, True),
    (2.35, 1.1, 0.5, 5.2, True)
])
def test_parameters_parsing_on_iris_model(sepalLength, sepalWidth, petalLength, petalWidth, validData):
    """
    Checks that the parsing of the parameters in the iris Model app is done correctly.
    It should return whether the data is valid depending on the input
    """
    featuresDict = {"sepalLength": sepalLength, "sepalWidth": sepalWidth,
                    "petalLength": petalLength, "petalWidth": petalWidth}
    if validData:
        assert parse(featuresDict) == ([sepalLength, sepalWidth, petalLength, petalWidth], True)
    else:
        assert parse(featuresDict) == ([], False)


def test_wrong_parameters_name_return_invalid():
    """
    Checks that if we pass invalid keys in the `features` dictionary, an exception is raised as it is detected
    as invalid data even if the values are correct. This applies to incorrect key names or to extra less
    parameters than desired
    """
    featuresDict = {"sepallength": 1.0, "ConfideNCE": 1.0,
                    "PETALLENGTH": 1.0, "peta": 1.0}
    featuresDict2 = {"iosdjfosjdfosij": 2.5}
    featuresDict3 = {"invalidKey": 1.0, "INVALIDKEY": 3.0}
    featuresDict4 = {"sepalLength": 1.0}
    featuresDict5 = {"sepalLength": 1.0, "sepalWidth": 1.0,
                     "petalLength": 1.0, "petalWidth": 1.0, "EXTRAKEY": 1.0}
    for features in [featuresDict, featuresDict2, featuresDict3, featuresDict4, featuresDict5]:
        assert parse(features) == ([], False)


@pytest.mark.parametrize("sepalLength,sepalWidth,petalLength,petalWidth", [
    (0.03, 3.1, 1.2, 0.7),
    (2.35, 1.1, 0.5, 5.2),
    (0.1, 2.1, 1.5, 3.2),
    (1.0, 2.1, 0.1, 0.1)
])
def test_prediction_for_valid_input(noParsingFeaturesNoPredictingModel, sepalLength,
                                    sepalWidth, petalLength, petalWidth):
    """
    Checks that the logic for prediction is correct in iris model. The prediction of the model is monkeypatched
    so that the model is not actually loaded. Also, the features are not actually parsed in this test,
    This test uses VALID parameters so a prediction is expected
    """
    sleep(0.1)
    inputFeatures = {"sepalLength": sepalLength, "sepalWidth": sepalWidth, "petalLength": petalLength,
                     "petalWidth": petalWidth}
    headers = {"Content-Type": "application/json"}
    outputDict = post("http://localhost:3000", data=json.dumps(inputFeatures), headers=headers).json()
    assert outputDict == {"predictedFlower": "Versicolor", "confidence": 0.85, "validData": True}


@pytest.mark.parametrize("sepalLength,sepalWidth,petalLength,petalWidth", [
    (1.0, 1.0, 1.0, 0.0),
    (None, None, None, None),
    (-0.1, 2.2, 0.3, 3.5),
    (3.2, None, -1, 0.4),
    (1.0, None, 1.0, 0.5)
])
def test_prediction_for_invalid_input(noParsingFeaturesNoPredictingModel, sepalLength,
                                      sepalWidth, petalLength, petalWidth):
    """
    Checks that the logic for prediction is correct in iris model. The prediction of the model is monkeypatched
    so that the model is not actually loaded. Also, the features are not actually parsed in this test
    This test uses INVALID parameters so a prediction SHOULD NOT BE RETURNED
    """
    sleep(0.1)
    inputFeatures = {"sepalLength": sepalLength, "sepalWidth": sepalWidth, "petalLength": petalLength,
                     "petalWidth": petalWidth}
    headers = {"Content-Type": "application/json"}
    outputDict = post("http://localhost:3000", data=json.dumps(inputFeatures), headers=headers).json()
    assert outputDict == {"validData": False}


def test_model_initialized_correctly():
    """
    Checks that the model.__init__ command loads the model and initialises both conversion dictionaries correctly
    """
    model = IrisModel()
    assert model.varietiesToNumbers == {"Versicolor": 0, "Setosa": 1, "Virginica": 2}
    assert model.varietiesToNumbers["Virginica"] == 2
    assert model.numbersToVarieties == {0: "Versicolor", 1: "Setosa", 2: "Virginica"}
    assert model.numbersToVarieties[1] == "Setosa"
    assert model.model is not None


def test_model_make_prediction():
    """
    Checks that the logic of the makePrediction function is correct
    """
    import random
    import numpy as np
    model = IrisModel()
    """
    We use random features each time
    (we could set a seed for reproducible results but then we would need a for loop
    to try with different inputs to see that the tests were not passes only by chance)
    """
    features = [random.uniform(0.01, 3) for i in range(4)]
    """
    model.model.predict is the prediction made directly by Keras without using our Class "makePrediction" method
    we need to use [0] as the predict method returns a two-dimensional array
    """
    rawPredictions = model.model.predict([features])[0]
    assert len(rawPredictions) == 3
    """
    predictedFlower and confidence are returned by "makePrediction" custom method of our IrisModel class
    confidence is returned as a percentage. Since it is the argmax, it should have at least 1/3 of 100%
    """
    predictedFlower, confidence = model.makePrediction(features)
    assert predictedFlower in ["Versicolor", "Setosa", "Virginica"]
    assert 100 >= confidence >= 33.3
    """
    We compare the prediction of our class, with a different way of computing the confidence to make sure
    that, if both are the same, our logic is working for sure
    """
    assert confidence == float(f"{np.max(rawPredictions)*100:.2f}")
    """
    Checks that the predicted Flower is the correct one according to the dictionaries in the __init__ method whose
    content has already been checked in the previous test
    """
    assert predictedFlower == model.numbersToVarieties[np.argmax(rawPredictions)]
