import pytest
import sys
import os
from requests import get, post
from time import sleep

sys.path.insert(0, ".")


def test_app_is_running(normalFrontend):
    """
    Checks that normal frontend is accessible on port 5000
    """
    sleep(0.1)
    assert 200 == get("http://localhost:5000").status_code


def test_index_template_is_rendered(normalFrontend):
    """
    Checks that the index template with the form is rendered succesfully when accessing "/" route
    """
    sleep(0.1)
    assert "Make Prediction" in get("http://localhost:5000").text


def test_get_results_catches_connection_exception(normalFrontend):
    """
    Checks that even if the frontend does not have connection to MySQL,
    it does not crash when accessing previous predictions.
    Instead, it returns empty results.
    """
    sleep(0.1)
    assert 200 == get("http://localhost:5000/database").status_code
    assert "Confidence(%)</h3>\n\n</body>" in get("http://localhost:5000/database").text


@pytest.mark.parametrize("sepalLength,sepalWidth,petalLength,petalWidth", [
    (1, 1, 1, 1),
    (2.3, 0.1, 99, 5),
    (3, 1.2, 0.2, 0.1)
])
def test_render_template_results_correct_inputs(frontEndDoesNotPostInputToBackend, sepalLength, sepalWidth,
                                                petalLength, petalWidth):
    """
    Makes sure that the main logic inside the FrontEnd works by monkeypatching the connection to the backend.
    A fake response from the model is received and rendered.
    In this test we use correct inputs and check that rendered template is correct
    """
    sleep(0.1)
    renderedhtml = post("http://localhost:5000", data={"sepalLength": sepalLength, "sepalWidth": sepalWidth,
                                                       "petalLength": petalLength, "petalWidth": petalWidth}).text
    assert "Confidence of the prediction: 0.99" in renderedhtml and "The flower is Virginica" in renderedhtml


@pytest.mark.parametrize("sepalLength,sepalWidth,petalLength,petalWidth", [
    (None, 1, 1, 1),
    (2.3, 0.1, None, 5),
    (3, 1.2, -0.2, 0.1)
])
def test_render_template_results_wronginputs(frontEndDoesNotPostInputToBackend, sepalLength, sepalWidth,
                                             petalLength, petalWidth):
    """
    Makes sure that the main logic inside the FrontEnd works by monkeypatching the connection to the backend.
    A fake response from the model is received and rendered.
    In this test we use wrong inputs
    """
    sleep(0.1)
    renderedhtml = post("http://localhost:5000", data={"sepalLength": sepalLength, "sepalWidth": sepalWidth,
                                                       "petalLength": petalLength, "petalWidth": petalWidth}).text
    assert "Please enter positive numeric values in all fields" in renderedhtml
