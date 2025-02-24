DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;

CREATE TABLE users (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT        NOT NULL,
    age   INTEGER     NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE products (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT    NOT NULL,
    price REAL    NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL,
    total_price REAL    NOT NULL,
    order_date  TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

INSERT INTO users (name, age, email)
VALUES ('Alice', 30, 'alice@example.com'),
       ('Bob', 25, 'bob@example.com'),
       ('Charlie', 40, 'charlie@example.com'),
       ('David', 35, 'david@example.com'),
       ('Eve', 28, 'eve@example.com');

INSERT INTO products (name, price, stock)
VALUES ('Laptop', 999.99, 10),
       ('Smartphone', 499.99, 20),
       ('Tablet', 299.99, 15),
       ('Headphones', 99.99, 50),
       ('Keyboard', 49.99, 30);

INSERT INTO orders (user_id, product_id, quantity, total_price)
VALUES (1, 1, 1, 999.99),
       (2, 3, 2, 599.98),
       (3, 2, 1, 499.99),
       (4, 4, 3, 299.97),
       (5, 5, 1, 49.99);
