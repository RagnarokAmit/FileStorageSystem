CREATE DATABASE file_storage;

USE file_storage;


CREATE TABLE users
(
    id INT PRIMARY KEY AUTO_INCREMENT,

    username VARCHAR(50) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL
);



CREATE TABLE files
(
    id INT PRIMARY KEY AUTO_INCREMENT,

    user_id INT NOT NULL,

    filename VARCHAR(255) NOT NULL,

    filepath VARCHAR(500) NOT NULL,

    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    FOREIGN KEY(user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);