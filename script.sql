
USE julio;

DROP TABLE BrewOrder;
DROP TABLE BrewRound;
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
    FOREIGN KEY (favourite_drink_id) REFERENCES Drink(drink_id)
); 


CREATE TABLE BrewRound
(
    round_id INTEGER AUTO_INCREMENT PRIMARY KEY, 
    is_open BOOLEAN, 
    brewer INTEGER,
    open_date DATETIME,
   	FOREIGN KEY (brewer) REFERENCES Person(person_id)
); 

CREATE TABLE BrewOrder
(
    order_id INTEGER AUTO_INCREMENT PRIMARY KEY, 
    drink_id INTEGER,
    person_id INTEGER,
    round_id INTEGER,
    FOREIGN KEY (drink_id) REFERENCES Drink(drink_id),
    FOREIGN KEY (person_id) REFERENCES Person(person_id),
    FOREIGN KEY (round_id) REFERENCES BrewRound(round_id)
); 



INSERT INTO Drink(name) VALUES ('Water'),('Coffee'),('Tea');


INSERT INTO julio.Person(name,favourite_drink_id) VALUES ('Eduardo', 1), ('Julio', 1), ('Henry', 3);

INSERT INTO BrewRound(is_open,brewer,open_date) VALUES (FALSE, 1, CURRENT_TIMESTAMP), (FALSE, 2, CURRENT_TIMESTAMP), (TRUE, 2, CURRENT_TIMESTAMP);

INSERT INTO BrewOrder(drink_id, person_id, round_id) VALUES (1,2,1), (2,1,1), (3,1,2), (1,3,2), (1,2,2), (1,2,3);






