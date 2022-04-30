CREATE DATABASE IF NOT EXISTS irisdatabase;
use irisdatabase;
CREATE TABLE IF NOT EXISTS iristable (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, sepalLength FLOAT NOT NULL, sepalWidth FLOAT NOT NULL, petalLength FLOAT NOT NULL, petalWidth FLOAT NOT NULL, predictedFlower Varchar (20), confidence FLOAT);
GRANT ALL PRIVILEGES ON irisdatabase.iristable TO 'webapp'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
