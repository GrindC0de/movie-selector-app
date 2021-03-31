

DROP DATABASE IF EXISTS  movie_select;

CREATE DATABASE movie_select;

\c movie_select

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
  film_name TEXT NOT NULL,
  rating DATE
);