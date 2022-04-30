from flask import Flask, request, render_template
import os
import requests
import json

app = Flask(__name__)


@app.route("/database", methods=["GET"])
def getlastresults():
    results = None
    try:
        # QUERY SHOULD BE EXECUTED ON BACKEND
        results = requests.get("http://backend:8080/lastresults").json()

    except Exception as e:
        print(f" There was an error when executing the query {e}")
    return render_template("lastresults.html", results=results)


@app.route("/", methods=["GET", "POST"])
def inputform():
    if request.method == "GET":
        return render_template("index.html")

    else: #request.method == "POST"
        # data = json.dumps({"SepalLength":"1.0","SepalWidth":"1.0","PetalLength":"1.0","PetalWidth":"1.0"})
        sepalLength = request.form.get("sepalLength", "-1.0")
        sepalWidth = request.form.get("sepalWidth", "-1.0")
        petalLength = request.form.get("petalLength", "-1.0")
        petalWidth = request.form.get("petalWidth", "-1.0")
        features = {"sepalLength": sepalLength, "sepalWidth": sepalWidth, "petalLength": petalLength,
                    "petalWidth": petalWidth}
        headers = {"Content-Type": "application/json"}
        response = requests.post("http://backend:8080", data=json.dumps(features), headers=headers)
        data = response.json()

        if data['validData']:
            return render_template("results.html", data=data)
        else:
            return render_template("wrongInput.html")


if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
