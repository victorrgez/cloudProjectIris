import pymysql

connection = pymysql.connect(
  host="localhost",
  user="webapp",
  password="webapp",
  database="irisdatabase"
)

cursor = connection.cursor()

values = [1.0, 2.0, 3.0, 4.0]

templateQuery = f'INSERT INTO iristable (sepalLength, sepalWidth, petalLength, petalWidth) VALUES({values[0]}, {values[1]}, {values[2]}, {values[3]});'


try:
        cursor.execute(templateQuery)
        connection.commit()
except Exception as e:
	print (f" There was an error when executing the query {e}")