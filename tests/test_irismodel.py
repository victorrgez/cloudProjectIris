from requests import get, post
from time import sleep
from src.irismodel3000.main import parse
import pytest
"""
Make sure we install the requirements on "src/irismodel3000/requirements.txt"
for carrying out these tests since we will need Tensorflow
(not installing TF before in order not to slow down the rest of the tests)
"""

def test_iris_model_is_reachable(normalModel):
    """
    Makes sure that the standard version of the Iris model without monkeypatching
    can be brought up succesfully and that it is reachable through a POST request
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
