from flask import Flask, request
import os
import requests
import json
import pymysql

app = Flask(__name__)
connection = pymysql.connect(
    host="localhost",
    user="webapp",
    password="webapp",
    database="irisdatabase",
    port=3306
)

cursor = connection.cursor()


@app.route("/lastresults", methods=["GET"])
def sendlastresults():
    try:
        lastResultsQuery = 'SELECT * from irisdatabase.iristable ORDER BY ID DESC;'
        cursor.execute(lastResultsQuery)
        connection.commit()
        results = cursor.fetchall()
        return json.dumps(results)
    except Exception as e:
        print(f" There was an error when executing the query {e}")
        return {}


@app.route("/", methods=["POST"])
def predictandinsert():
    # data = json.dumps({"SepalLength":"1.0","SepalWidth":"1.0","PetalLength":"1.0","PetalWidth":"1.0"})
    features = request.get_json()
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://localhost:3000", data=json.dumps(features), headers=headers)
    results = response.json()
    if results['validData']:
        try:
            templateQuery = f'INSERT INTO irisdatabase.iristable (sepalLength, sepalWidth, petalLength, petalWidth, predictedFlower, confidence) VALUES({features["sepalLength"]}, {features["sepalWidth"]}, {features["petalLength"]}, {features["petalWidth"]}, \'{results["predictedFlower"]}\', {results["confidence"]});'
            cursor.execute(templateQuery)
            connection.commit()
        except Exception as e:
            print(f" There was an error when executing the query {e}")

    return results


if (__name__ == "__main__"):
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
