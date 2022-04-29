from flask import Flask, request, render_template
import os
import requests
import json
import pymysql

app = Flask(__name__)
connection = pymysql.connect(
    host="localhost",
    user="webapp",
    password="webapp",
    database="irisdatabase"
)

cursor = connection.cursor()


@app.route("/database", methods=["GET"])
def showlastresults():
    try:
        lastResultsQuery = 'SELECT * from irisdatabase.iristable ORDER BY ID DESC;'
        cursor.execute(lastResultsQuery)
        connection.commit()
        results = cursor.fetchall()
    except Exception as e:
        print(f" There was an error when executing the query {e}")
    return render_template("lastresults.html", results = results)


@app.route("/", methods=["GET", "POST"])
def iris():
    if request.method == "GET":
        return render_template("index.html")

    else:
        # data = json.dumps({"SepalLength":"1.0","SepalWidth":"1.0","PetalLength":"1.0","PetalWidth":"1.0"})
        sepalLength = request.form.get("sepalLength", "-1.0")
        sepalWidth = request.form.get("sepalWidth", "-1.0")
        petalLength = request.form.get("petalLength", "-1.0")
        petalWidth = request.form.get("petalWidth", "-1.0")
        features = {"sepalLength": sepalLength, "sepalWidth": sepalWidth, "petalLength": petalLength,
                    "petalWidth": petalWidth}
        headers = {"Content-Type": "application/json"}
        response = requests.post("http://localhost:3000", data=json.dumps(features), headers=headers)

        if response.json()['validData']:
            try:
                data = response.json()
                templateQuery = f'INSERT INTO irisdatabase.iristable (sepalLength, sepalWidth, petalLength, petalWidth, predictedFlower, confidence) VALUES({features["sepalLength"]}, {features["sepalWidth"]}, {features["petalLength"]}, {features["petalWidth"]}, \'{data["predictedFlower"]}\', {data["confidence"]});'
                cursor.execute(templateQuery)
                connection.commit()
            except Exception as e:
                print(f" There was an error when executing the query {e}")

            return render_template("results.html", data=data)
        else:
            return render_template("wrongInput.html")


if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
