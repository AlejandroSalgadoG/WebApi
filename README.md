Api with token auth

docker build -t token:latest .
docker run -p 8000:8000 --rm -it token uv run src/manage.py runserver 0.0.0.0:8000

docker-compose run -p 8000:8000 --rm app
