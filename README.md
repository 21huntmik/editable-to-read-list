# f20-authentication-21huntmik
f20-authentication-21huntmik created by GitHub Classroom

# My Authentication Project

## Resource
### Books
Attributes:
* title (string)
* author (string)
* pages (string)
* year (string)
* genre (string)

### Users
Attributes:
* email (string)
* password (string)
* fname (string)
* lname (string)

## Schema
CREATE TABLE books (
id INTEGER PRIMARY KEY,
title TEXT,
author TEXT,
date TEXT,
genre TEXT);

CREATE TABLE users (
id INTEGER PRIMARY KEY,
email TEXT,
password TEXT,
fname TEXT,
lname TEXT);

## REST Endpoints
Name | Method | Path
-----|--------|-----
Retrieve book collection | GET | /books
Retrieve book member | GET | /books/id
Create book member | POST | /books
Update restaurant member | PUT | /books/id
Delete restaurant member | DELETE | /books/id
Create user member | POST | /users
Create session | POST | /sessions
Delete session | DELETE | /sessions

## Encryption
I used bcrypt with the standard parameters
