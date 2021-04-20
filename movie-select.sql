

DROP DATABASE IF EXISTS  movie-select;

CREATE DATABASE movie-select;

\c movie-select

CREATE TABLE users
(
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE rated_movies
(
  id SERIAL PRIMARY KEY,
  user_id SERIAL REFERENCES users(id),
  title TEXT NOT NULL,
  rating INTEGER
);