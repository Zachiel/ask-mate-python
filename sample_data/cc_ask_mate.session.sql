CREATE TABLE IF NOT EXISTS accounts (
    id serial NOT NULL,
    username varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    email varchar(100),
    PRIMARY KEY (id)

);