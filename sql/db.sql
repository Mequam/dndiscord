CREATE DATABASE dndiscord;

\c dndiscord

CREATE TABLE player(
	plaNum SERIAL PRIMARY KEY,
	plaName VARCHAR(10),
	plaTag VARCHAR(40)
);

CREATE TABLE race(
	racName CHAR(10) PRIMARY KEY,
	racDesc VARCHAR(40) 
);

CREATE TABLE stat(
	emoji CHAR(1) PRIMARY KEY,
	staName CHAR(10),
	staDesc VARCHAR(40),
	staGen VARCHAR(40),
	staRoll CHAR(40) -- represents the way the roll is outputed 
);

CREATE TABLE charicter(
	chaNum SERIAL PRIMARY KEY,
	chaName VARCHAR(10),
	plaNum INT REFERENCES player,
	racName VARCHAR(10) REFERENCES race
);

CREATE TABLE cha2sta(
	emoji CHAR(1) REFERENCES stat,
	chaNum INT REFERENCES charicter,
	value INT NOT NULL,
	PRIMARY KEY (emoji,chaNum)
);

CREATE TABLE game(
	gamId SERIAL PRIMARY KEY,
	gamName char(20),
	gamDesc VARCHAR(60)
);
CREATE TABLE game2cha(
	gamId INT REFERENCES game,
	chaID INT REFERENCES charicter,
	gamR boolean NOT NULL,
	gamW boolean NOT NULL,
	gamD boolean NOT NULL,
	dmR boolean NOT NULL,
	dmW boolean NOT NULL,
	dmD boolean NOT NULL	
);

CREATE USER dm WITH LOGIN;

GRANT SELECT ON player TO dm;
GRANT INSERT ON player TO dm;
GRANT UPDATE ON player TO dm;
GRANT DELETE ON player TO dm;

GRANT SELECT ON race TO dm;
GRANT INSERT ON race TO dm;
GRANT UPDATE ON race TO dm;
GRANT DELETE ON race TO dm;

GRANT SELECT ON stat TO dm;
GRANT INSERT ON stat TO dm;
GRANT UPDATE ON stat TO dm;
GRANT DELETE ON stat TO dm;

GRANT SELECT ON charicter TO dm;
GRANT INSERT ON charicter TO dm;
GRANT UPDATE ON charicter TO dm;
GRANT DELETE ON charicter TO dm;

GRANT SELECT ON cha2sta TO dm;
GRANT INSERT ON cha2sta TO dm;
GRANT UPDATE ON cha2sta TO dm;
GRANT DELETE ON cha2sta TO dm;

