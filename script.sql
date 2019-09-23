DROP TABLE Drink;
DROP TABLE Person;

CREATE TABLE Drink
(
    drink_id INTEGER AUTO_INCREMENT PRIMARY KEY, 
    name VARCHAR(100)
); 


CREATE TABLE Person
(
    person_id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (100),
    favorite_drink_id INTEGER,
    FOREIGN KEY (favorite_drink_id) REFERENCES Drink(drink_id)
); 


INSERT INTO Drink(name) VALUES ('Water')

INSERT INTO People(name,favorite_drink_id) VALUES ('Eduardo', 1)