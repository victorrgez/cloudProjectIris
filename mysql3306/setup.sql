CREATE DATABASE irisdatabase;
use irisdatabase;
CREATE TABLE iristable (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, sepalLength FLOAT NOT NULL, sepalWidth FLOAT NOT NULL, petalLength FLOAT NOT NULL, petalWidth FLOAT NOT NULL);
GRANT ALL PRIVILEGES ON irisdatabase.iristable TO 'webapp'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;