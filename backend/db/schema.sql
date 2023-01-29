DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS mtweets;
DROP TABLE IF EXISTS contact;

CREATE TABLE users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TimeStamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FName TEXT NOT NULL,
    LName TEXT NOT NULL,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL,
    Salt TEXT NOT NULL,
    Session TEXT DEFAULT 'session',
    OTP INTEGER DEFAULT 1,
    Verified INTEGER DEFAULT 0
);

CREATE TABLE mtweets (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TimeStamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UserID TEXT NOT NULL,
    Tweet TEXT NOT NULL,
    Result TEXT NOT NULL,
    CompoundCore TEXT NOT NULL,
    Negative TEXT NOT NULL,
    Neutral TEXT NOT NULL,
    Positive TEXT NOT NULL
);

CREATE TABLE contact (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TimeStamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FName TEXT NOT NULL,
    Lname TEXT NOT NULL,
    Email TEXT NOT NULL,
    Brief TEXT NOT NULL
);