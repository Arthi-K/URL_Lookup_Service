DROP TABLE IF EXISTS url_table;

CREATE TABLE url_table(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    url_addr TEXT NOT NULL,
    content TEXT NOT NULL
);