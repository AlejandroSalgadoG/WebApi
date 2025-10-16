FROM python:3.12-alpine3.22

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

WORKDIR /api

COPY pyproject.toml /api
COPY uv.lock /api

RUN pip install uv && \
    uv sync && \
    adduser --disabled-password django-user

USER django-user

EXPOSE 8000
