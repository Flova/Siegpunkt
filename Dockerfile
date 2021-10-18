FROM python:3.9

ADD . /Siegpunkt

WORKDIR /Siegpunkt/siegpunkt

RUN pip install poetry

RUN poetry run pip install 'setuptools==57.5.0' # Fix for https://github.com/elimintz/justpy/issues/301

RUN poetry install

EXPOSE 8000

CMD poetry run alembic upgrade head; poetry run uvicorn --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips="*" app:app
