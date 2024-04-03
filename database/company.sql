DROP TABLE IF EXISTS users;
CREATE TABLE users(
    user_pk                 TEXT,
    user_email              TEXT  UNIQUE,
    user_password           TEXT,
    user_verified         INTEGER,
    user_verification_id    TEXT,
    PRIMARY KEY(user_pk)
) WITHOUT ROWID;



-- SEED
INSERT INTO users VALUES("1","one@one.com", "password",0, "1rrwerwerer");


SELECT * FROM users;    
