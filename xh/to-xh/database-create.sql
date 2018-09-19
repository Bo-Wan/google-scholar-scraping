CREATE TABLE article (
    id INT NOT NULL,
    journal VARCHAR(255),
    dates VARCHAR(255),
    title VARCHAR(255),
    author VARCHAR(255),
    citation INT,
    http_code INT,
    PRIMARY KEY (id)
);
