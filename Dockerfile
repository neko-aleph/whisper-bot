FROM python:3.13.4-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry && poetry install --no-root

COPY . /app

ENTRYPOINT ["poetry", "run", "python", "-m", "whisper_bot.run"]