CREATE TABLE IF NOT EXISTS accounts (
    id serial NOT NULL,
    username varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    fname varchar(100),
    lname varchar(100),
    registrationDate date,
    PRIMARY KEY (id)

);