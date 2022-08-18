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
    """
    Sends a Get request to "/lastresults" route of the backend model. Instead of actually connecting to MySQL,
    it returns fake rows that would represent the last predictions of the model.
    This checks that the logic in the backend is correct as well as the format of the data returned
    """
    sleep(0.1)
    fakeResults = [[1, 1.1, 0.1, 3.2, 1.2, "Virginica", 0.90],
                   [2, 0.03, 3.1, 1.2, 0.7, "Versicolor", 0.90],
                   [3, 2.35, 1.1, 0.5, 5.2, "Setosa", 0.85]]
    renderedHTML = get("http://localhost:8080/lastresults").text
    assert json.dumps(fakeResults) == renderedHTML


def test_model_prediction_backend_to_frontend_correct_format(backendNoConnectionMySQLnorModel):
    """
    Pretends that the frontend is sending some features to the backend to get a prediction from the ML model.
    It returns (in the reponse to the initial request) a fake prediction  that includes the flower and the confidence
    The inclusion of this prediction in the MySQL database is skipped with monkeypatching as we are only testing and
    we do not have a connection to the database active.
    """
    sleep(0.1)
    features = json.dumps({"SepalLength": "1.0", "SepalWidth": "1.0",
                           "PetalLength": "1.0", "PetalWidth": "1.0"})
    headers = {"Content-Type": "application/json"}
    renderedHTML = post("http://localhost:8080/", data=features, headers=headers).text
    assert {"predictedFlower": "Virginica", "confidence": 0.99, "validData": True} == json.loads(renderedHTML)
