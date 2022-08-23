import requests


def test_get_empty_database_make_two_predictions_get_last_results():
    """
    First, we request last results when there are no predictions in the database. Therefore, no previous results
    are rendered, and we get `Confidence(%)</h3>\n\n</body>` in the rendered template
    (otherwise there would be rows in the middle before reaching `</body>`)

    Then we make a couple of predictions, and we assert that in the last call to /database route we are getting rows
    corresponding to both past predictions.
    """
    # First call to empty database:
    renderedEmptyResults = requests.get("http://localhost:5000/database").text
    assert "Confidence(%)</h3>\n\n</body>" in renderedEmptyResults

    # First prediction:
    firstPredictedResults = requests.post("http://localhost:5000", data={"sepalLength": 0.5, "sepalWidth": 1.2,
                                                                         "petalLength": 1.1, "petalWidth": 0.5}).text
    assert "Confidence of the prediction" in firstPredictedResults and "The flower is" in firstPredictedResults

    # Calling database with only one row:
    nonEmptyResults = requests.get("http://localhost:5000/database").text
    assert ("Setosa" in nonEmptyResults or "Virginica" in nonEmptyResults
            or "Setosa" in nonEmptyResults) and 1.2 in nonEmptyResults

    # Second prediction:
    secondPredictedResults = requests.post("http://localhost:5000", data={"sepalLength": 1.5, "sepalWidth": 2.2,
                                                                          "petalLength": 0.7, "petalWidth": 3.5}).text
    assert "Confidence of the prediction" in secondPredictedResults and "The flower is" in secondPredictedResults

    # Calling database with the two rows already added:
    bothPredictedResults = requests.get("http://localhost:5000/database").text
    assert ("Setosa" in bothPredictedResults or "Virginica" in bothPredictedResults
            or "Setosa" in bothPredictedResults) and 1.1 in bothPredictedResults and 3.5 in bothPredictedResults
