from irismodel import IrisModel
from flask import Flask, request
import os


def parse(receivedDict):
    validData = True
    try:
        if (set(receivedDict.keys()) != set(["sepalLength", "sepalWidth", "petalLength", "petalWidth"])):
            raise Exception

        SepalLength = float(receivedDict.get("sepalLength"))
        SepalWidth = float(receivedDict.get("sepalWidth"))
        PetalLength = float(receivedDict.get("petalLength"))
        PetalWidth = float(receivedDict.get("petalWidth"))
        features = [SepalLength, SepalWidth, PetalLength, PetalWidth]

        for value in features:
            if float(value) <= 0:
                raise Exception
    except:
        validData= False
        return [], validData

    features = [SepalLength, SepalWidth, PetalLength, PetalWidth]
    return features, validData


app = Flask(__name__)


@app.route("/", methods=["POST"])
def predict():
    receivedDict = request.get_json()
    features, validData = parse(receivedDict)
    if validData:
        predictedFlower, confidence = model.makePrediction(features)
        return {"predictedFlower": predictedFlower, "confidence": confidence, "validData": True}
    else:
        return {"validData": False}


if (__name__ == "__main__"):
    model = IrisModel()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
    """
    Works Sending the Following from a terminal:
    curl -X POST localhost:3000 -H 'Content-Type:application/json' -d '{"sepalLength":"1.0","sepalWidth":"1.0","petalLength":"1.0","petalWidth":"1.0"}'
    
    Or we can send this from a Pythons script:
    import requests
    import json
    data = json.dumps({"sepalLength":"1.0","sepalWidth":"1.0","petalLength":"1.0","petalWidth":"1.0"})
    headers = {"Content-Type":"application/json"}
    response = requests.post("http://localhost:3000", data=data, headers=headers)
    print (response.json())
    """

