from requests import get, post
from time import sleep


def test_backend_reachable(normalBackend):
    """
    Checks that the backend is up and running. It returns a simple html when doing a get request to the root directory:
    `<html><body>APP IS UP AND RUNNING</body></html>` that servers as a health check.
    """
    sleep(0.1)
    assert 200 == get("http://localhost:8080").status_code
    assert "<html><body>APP IS UP AND RUNNING</body></html>" == get("http://localhost:8080").text
