import pymysql

connection = pymysql.connect(
  host="localhost",
  user="webapp",
  password="webapp",
  database="irisdatabase"
)

cursor = connection.cursor()

features = {"sepalLength":1.0, "sepalWidth":2.0, "petalLength":3.0, "petalWidth":4.0}
data={"predictedFlower":"Virginica", "confidence":3.25}

#templateQuery = f'INSERT INTO iristable (sepalLength, sepalWidth, petalLength, petalWidth, predictedFlower, confidence) VALUES({features["sepalLength"]}, {features["sepalWidth"]}, {features["petalLength"]}, {features["petalWidth"]}, \'{data["predictedFlower"]}\', {data["confidence"]});'
templateQuery = 'SELECT * from irisdatabase.iristable ORDER BY ID DESC;'

try:
        cursor.execute(templateQuery)
        connection.commit()
        results = cursor.fetchall()
        print (results)
        print (type(results))
except Exception as e:
	print (f" There was an error when executing the query {e}")
