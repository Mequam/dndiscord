CREATE DATABASE dndiscord;

\c dndiscord

CREATE TABLE player(
	plaNum SERIAL PRIMARY KEY,
	plaName VARCHAR(10),
	plaTag VARCHAR(10)
);

CREATE TABLE race(
	racName VARCHAR(10) PRIMARY KEY,
	racDesc VARCHAR(40) 
);

CREATE TABLE stat(
	staName VARCHAR(10) PRIMARY KEY,
	staDesc VARCHAR(40),
	staGen VARCHAR(40)
);

CREATE TABLE charicter(
	chaNum SERIAL PRIMARY KEY,
	chaName VARCHAR(10),
	plaNum INT REFERENCES player,
	racName VARCHAR(10) REFERENCES race
);

-- need to figure out how to make a dual primary key for postgresql

CREATE TABLE cha2sta(
	staName VARCHAR(10) REFERENCES stat,
	chaNum INT REFERENCES charicter
);
