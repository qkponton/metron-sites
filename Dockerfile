# pull the official base image
FROM python:3.10

ARG USER_HOME=/home/opsuser

USER root

RUN adduser --gecos "First Last,RoomNumber,WorkPhone,HomePhone" --disabled-password opsuser \
    && mkdir -p /log/app \
    && chown opsuser:opsuser /log/app \
    && mkdir -p /app \
    && chown opsuser:opsuser /app \
    && chmod -R 755 /app \
    && mkdir -p /vol/web/static \
    && mkdir -p /vol/web/media \
    && chown -R opsuser:opsuser /vol \
    && chmod -R 755 /vol

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 # prevents Python from copying pyc files to the container.
ENV PYTHONUNBUFFERED 1 #  ensures that Python output is logged to the terminal, making it possible to monitor Django logs in realtime.

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

# install dependencies
RUN pip install --upgrade pip && \
    pip install poetry

# set work directory
USER opsuser
WORKDIR /app

# copy project
COPY --chown=opsuser:opsuser . /app

RUN poetry install

ENTRYPOINT ["./entrypoint.sh"]

CMD ["poetry", "run", "python", "-m", "metron_sites"]
