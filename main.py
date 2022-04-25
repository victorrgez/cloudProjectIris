from irismodel import IrisModel
from flask import Flask, request
import os


def parse(receivedDict):
    SepalLength = float(receivedDict.get("SepalLength"))
    SepalWidth = float(receivedDict.get("SepalWidth"))
    PetalLength = float(receivedDict.get("PetalLength"))
    PetalWidth = float(receivedDict.get("PetalWidth"))
    features = [SepalLength, SepalWidth, PetalLength, PetalWidth]
    return features


app = Flask(__name__)


@app.route("/", methods=["POST"])
def predict():
    receivedDict = request.get_json()
    features = parse(receivedDict)
    predictedFlower, confidence = model.makePrediction(features)
    return f"<html><h3>The flower is {predictedFlower}. The confidence is {confidence:.2f}%.</h3></html>"


if (__name__ == "__main__"):
    model = IrisModel()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    """
    Works Sending the Following:
    curl -X POST localhost:5000 -H 'Content-Type:application/json' -d '{"SepalLength":"1.0","SepalWidth":"1.0","PetalLength":"1.0","PetalWidth":"1.0"}'
    """

