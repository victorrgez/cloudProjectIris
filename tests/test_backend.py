from requests import get, post
from time import sleep
import json


def test_backend_reachable(normalBackend):
    """
    Checks that the backend is up and running. It returns a simple html when doing a get request to the root directory:
    `<html><body>APP IS UP AND RUNNING</body></html>` that servers as a health check.
    """
    sleep(0.1)
    assert 200 == get("http://localhost:8080").status_code
    assert "<html><body>APP IS UP AND RUNNING</body></html>" == get("http://localhost:8080").text


def test_last_results_returned_to_frontend(backendNoConnectionMySQLnorModel):
    sleep(0.1)
    fakeResults = [[1, 1.1, 0.1, 3.2, 1.2, "Virginica", 0.90],
                   [2, 0.03, 3.1, 1.2, 0.7, "Versicolor", 0.90],
                   [3, 2.35, 1.1, 0.5, 5.2, "Setosa", 0.85]]
    renderedHTML = get("http://localhost:8080/lastresults").text
    assert json.dumps(fakeResults) == renderedHTML


def test_model_predicition_back_to_frontend_correct_format(backendNoConnectionMySQLnorModel):
    sleep(0.1)
    renderedHTML = get("http://localhost:8080/lastresults").text
    assert '{"predictedFlower": "Virginica", "confidence": 0.99, "validData": True}' == renderedHTML
