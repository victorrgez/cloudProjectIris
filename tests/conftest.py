import pytest
from multiprocessing import Process
import sys
import os
import json

sys.path.insert(0, ".")
from src.frontend5000.main import app

"""
This file contains all the fixtures used in the tests
"""


@pytest.fixture
def normalFrontend():
    """
    Executes the normal Frontend in the background without monkeypatching anything
    """
    server = Process(target=app.run, args=("0.0.0.0", int(os.environ.get("PORT", 5000))))
    server.start()
    yield
    server.terminate()
    server.join()


@pytest.fixture
def frontEndMocksLastModelResults(monkeypatch):
    """
    Mocks the connection to backend and to MySQL database and returns fake previous results predicted by the Model.
    The `json` function from `requests.get.json()` in `src.frontend5000.main` is also mocked
    """
    class FakeRowsResponse:
        def __init__(self):
            self.fakeRows = [[1, 1.1, 0.1, 3.2, 1.2, "Virginica", 0.90],
                             [2, 0.03, 3.1, 1.2, 0.7, "Versicolor", 0.90],
                             [3, 2.35, 1.1, 0.5, 5.2, "Setosa", 0.85]]

        def json(self):
            return self.fakeRows

    monkeypatch.setattr("src.frontend5000.main.requests.get", lambda url: FakeRowsResponse())
    server = Process(target=app.run, args=("0.0.0.0", int(os.environ.get("PORT", 5000))))
    server.start()
    yield
    server.terminate()
    server.join()


@pytest.fixture
def frontEndDoesNotPostInputToBackend(monkeypatch):
    """
    Instead of sending the input from the Form of the Flask APP to the Backend, we build a fake Backend response.
    We monkeypatch `request.post`, and need to create a custom Class so that
    `response.json()` from `src.frontend5000.main` can achieve its goal.
    We also do some quick parameter checking to return in the fake response from Backend if the data is valid or not.
    """

    class ResponseWithJsonMethod:
        def __init__(self, data):
            """
            Receives a dictonary with the inputs.
            Creates a `wrongInput` list that will be empty if all input parameters are valid
            """

            data = json.loads(data)
            wrongInput = [attribute for attribute in data.values() if attribute is None or float(attribute) <= 0.0]

            if not wrongInput:
                print("VALID")
                self.response = {"predictedFlower": "Virginica", "confidence": 0.99, "validData": True}
            else:
                print("INVALID")
                self.response = {"predictedFlower": "Virginica", "confidence": 0.99, "validData": False}

        def json(self):
            """
            Response.json() will return the dictionary
            """
            return self.response

    monkeypatch.setattr("src.frontend5000.main.requests.post", lambda url, data, headers: ResponseWithJsonMethod(data))

    server = Process(target=app.run, args=("0.0.0.0", int(os.environ.get("PORT", 5000))))
    server.start()
    yield
    server.terminate()
    server.join()
