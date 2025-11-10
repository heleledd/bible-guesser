FROM python:3.12-slim-bookworm

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./.env /code/.env

CMD ["fastapi", "run", "app/main.py", "--port", "80"]