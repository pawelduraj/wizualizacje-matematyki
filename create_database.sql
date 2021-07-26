DROP EXTENSION IF EXISTS citext CASCADE;
DROP EXTENSION IF EXISTS pgcrypto CASCADE; 
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS questions CASCADE; 
DROP TABLE IF EXISTS answers CASCADE; 

CREATE EXTENSION citext;
CREATE EXTENSION pgcrypto;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name NAME NOT NULL UNIQUE,
    passw TEXT NOT NULL,
    mail CITEXT NOT NULL UNIQUE,
    points INTEGER NOT NULL
);

CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    question TEXT NOT NULL
);

CREATE TABLE answers (
    answer_id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL,
    answer TEXT NOT NULL,
    is_good BOOLEAN NOT NULL,
    CONSTRAINT fk_question
        FOREIGN KEY (question_id)
            REFERENCES questions (question_id)
            ON DELETE CASCADE
);
