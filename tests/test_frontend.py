import pytest
from multiprocessing import Process
import sys
import os
import requests
from time import sleep

sys.path.insert(0, ".")
from src.frontend5000.main import app
import src.frontend5000.main as frontend


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


def test_app_is_running(normalFrontend):
    """
    Checks that normal frontend is accessible on port 5000
    """
    sleep(0.1)
    assert 200 == requests.get("http://localhost:5000").status_code


def test_index_template_is_rendered(normalFrontend):
    """
    Checks that the index template with the form is rendered succesfully when accessing "/" route
    """
    sleep(0.1)
    assert "Make Prediction" in requests.get("http://localhost:5000").text


def test_get_results_catches_connection_exception(normalFrontend):
    """
    Checks that even if the frontend does not have connection to MySQL,
    it does not crash when accessing previous predictions.
    Instead, it returns empty results.
    """
    sleep(0.1)
    assert 200 == requests.get("http://localhost:5000/database").status_code
    assert "Confidence(%)</h3>\n\n</body>" in requests.get("http://localhost:5000/database").text


"""
NEED TO CHECK CONTENT OF VARIABLES IN THE OTHER SCRIPT
def test_wrong_input(normalFrontend):
    sleep(0.1)
    failure = requests.post("http://localhost:5000").text
    assert "123131" in failure
    assert frontend.sepalLength == -1
"""
