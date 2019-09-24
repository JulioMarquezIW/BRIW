
USE julio;

DROP TABLE Person;
DROP TABLE Drink;


CREATE TABLE Drink
(
    drink_id INTEGER AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100)
); 


CREATE TABLE Person
(
    person_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (100),
    favourite_drink_id INTEGER,
    FOREIGN KEY (favorite_drink_id) REFERENCES Drink(drink_id)
); 


INSERT INTO Drink(name) VALUES ('Water'),('Coffee'),('Tea');


INSERT INTO julio.Person(name,favorite_drink_id) VALUES ('Eduardo', 1), ('Julio', 1), ('Henry', 3);