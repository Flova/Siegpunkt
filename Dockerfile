FROM python:3.9

ADD . /Siegpunkt

WORKDIR /Siegpunkt/siegpunkt

RUN pip install poetry

RUN poetry install

CMD poetry run alembic upgrade head; poetry run python app.py
