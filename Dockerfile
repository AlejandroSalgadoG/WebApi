FROM python:3.12-alpine3.22

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

WORKDIR /app

COPY pyproject.toml /app
COPY uv.lock /app
COPY src /app/src

RUN pip install uv && \
    uv sync && \
    adduser --disabled-password django-user && \
    chown -R django-user:django-user /app

USER django-user

EXPOSE 8000
