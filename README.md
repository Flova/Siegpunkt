# Siegpunkt
A simple single page scoreboard web app written purely in Python

[![.github/workflows/main.yml](https://github.com/Flova/Siegpunkt/actions/workflows/main.yml/badge.svg)](https://github.com/Flova/Siegpunkt/actions/workflows/main.yml)

## About
The backend as well as the frontend of this single page web app is written purly in Python using [JustPy](https://github.com/elimintz/justpy).
Its used to keep track of the scorepoints over a long time if you play cards with your frinds.

## Screenshots
![Screenshot 2021-08-16 at 10-57-23 Siegpunkt](https://user-images.githubusercontent.com/15075613/129538784-0bd89949-720c-4b1c-ab49-12d19fd56b80.png)

## Install

Using docker 

```bash
docker pull flova/siegpunkt
docker run -d -p 8000:8000 -v <path_to_your_sqlite_file_location>:/Siegpunkt/siegpunkt/database/ siegpunkt
```

or using docker-compose

```yaml
version: '2'

services:
  siegpunkt:
     image: flova/siegpunkt:latest
     container_name: siegpunkt
     restart: always
     ports:
       - 8000:8000
     volumes:
       - <path_to_your_sqlite_file_location>:/Siegpunkt/siegpunkt/database
```

or manually

```bash
# Clone repo
git clone git@github.com:Flova/Siegpunkt.git
cd Siegpunkt
# Install deps
pip install poetry
poetry install
# Do migrations/create db
poetry run alembic upgrade head
# Run app
poetry run python siegpunkt/app.py
```
