CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(500) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL
);
