import pymysql
from time import sleep


def test_connection_to_mysql():
    """
    Test that checks that establishing a connection to mysql after having built and run the mysql image works
    The first SELECT statement should return Empty results while the second one should return one row that
    we have already inserted.
    Need to sleep a bit so that the MySQL database is up and running by the time the test is run
    """
    sleep(20)
    connection = pymysql.connect(host="localhost", user="webapp", password="webapp", database="irisdatabase", port=3306)
    cursor = connection.cursor()
    query = 'SELECT * from irisdatabase.iristable order by id desc limit 50;'
    cursor.execute(query)
    connection.commit()
    results = cursor.fetchall()
    assert (bool(results)) is False

    insertquery = 'INSERT INTO irisdatabase.iristable(sepallength, sepalwidth, petallength, petalwidth, ' \
                  'predictedflower, confidence) values (1.0, 1.0, 1.0, 1.0, "Virginica", 0.99); '
    cursor.execute(insertquery)
    selectquery = 'SELECT * from irisdatabase.iristable order by id desc limit 50;'
    cursor.execute(selectquery)
    connection.commit()

    results = cursor.fetchall()
    print(results)
    assert (bool(results)) is True
