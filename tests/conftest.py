import pytest
from multiprocessing import Process
import sys
import os
import json

sys.path.insert(0, ".")
from src.frontend5000.main import app as frontendAPP
from src.backend8080.main import app as backendAPP

"""
This file contains all the fixtures used in the tests. Index:
0.Fake Classes used
1.Frontend
2.Backend
3.IrisModel
"""

"""
0.Fake Classes used
"""


class FakeConnectionMySQL:
    """
    Chreates a fake connection to MySQL that will always return the same rows of the last results when
    executing the fetchall for any query
    """

    def __init__(self):
        self.fakeRows = [[1, 1.1, 0.1, 3.2, 1.2, "Virginica", 0.90],
                         [2, 0.03, 3.1, 1.2, 0.7, "Versicolor", 0.90],
                         [3, 2.35, 1.1, 0.5, 5.2, "Setosa", 0.85]]

    def cursor(self):
        return self

    def execute(self, queryString):
        pass

    def commit(self):
        pass

    def fetchall(self):
        return self.fakeRows


class FakeRowsResponse:
    """
    When executing an HTTP Request to an enpoint (backend, model, etc), we will return fake rows
    when doing Response.json()
    """

    def __init__(self):
        self.fakeRows = [[1, 1.1, 0.1, 3.2, 1.2, "Virginica", 0.90], [2, 0.03, 3.1, 1.2, 0.7, "Versicolor", 0.90],
                         [3, 2.35, 1.1, 0.5, 5.2, "Setosa", 0.85]]

    def json(self):
        return self.fakeRows


class ResponseWithJsonMethod:
    """
    Monkeypatching of the Model behaviour. This response to an HTTP request has the content of the model's prediction.
    Fakes the model predictions. Takes the user input and checkes whether they are valid and
    outputs the prediction when calling Response.json()
    """

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
            self.response = {"validData": False}

    def json(self):
        """
        Response.json() will return the dictionary
        """
        return self.response


"""
1. FRONTEND:
"""


@pytest.fixture
def normalFrontend():
    """
    Executes the normal Frontend in the background without monkeypatching anything
    """
    server = Process(target=frontendAPP.run, args=("0.0.0.0", int(os.environ.get("PORT", 5000))))
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

    monkeypatch.setattr("src.frontend5000.main.requests.get", lambda url: FakeRowsResponse())
    server = Process(target=frontendAPP.run, args=("0.0.0.0", int(os.environ.get("PORT", 5000))))
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
    We also do some quick parameter checking to return (in the fake response from Backend) if the data is valid or not.
    """

    monkeypatch.setattr("src.frontend5000.main.requests.post", lambda url, data, headers: ResponseWithJsonMethod(data))

    server = Process(target=frontendAPP.run, args=("0.0.0.0", int(os.environ.get("PORT", 5000))))
    server.start()
    yield
    server.terminate()
    server.join()


"""
2. BACKEND:
"""


@pytest.fixture
def normalBackend(monkeypatch):
    """
    Creates a normal backend without monkeypatching anything. Connection to MySQL has been moved to
    `if (__name__ == "__main__"):` so that it does not fail when importing the backend app.
    """
    server = Process(target=backendAPP.run, args=("0.0.0.0", int(os.environ.get("PORT", 8080))))
    server.start()
    yield
    server.terminate()
    server.join()


@pytest.fixture
def backendNoConnectionMySQLnorModel(monkeypatch):
    """
    Creates a backend that does not connect to MySQL nor the ML iris model.
    Instead, it returns fake model predictions (aftert doing some parameter checking to see if the input is valid)
    It also returns fake previous results from the model when the MySQL fake connection executes the "fetchall" method
    for a random query that would try to get the last model predictions.
    """
    features = {"SepalLength": "1.0", "SepalWidth": "1.0", "PetalLength": "1.0", "PetalWidth": "1.0"}
    monkeypatch.setattr("src.backend8080.main.pymysql.connect", lambda **kwargs: FakeConnectionMySQL())
    monkeypatch.setattr("src.backend8080.main.requests.post", lambda url, data, headers: ResponseWithJsonMethod(data))
    server = Process(target=backendAPP.run, args=("0.0.0.0", int(os.environ.get("PORT", 8080))))
    server.start()
    yield
    server.terminate()
    server.join()
