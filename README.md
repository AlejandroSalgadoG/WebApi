Api with token auth

docker build -t token:latest .
docker run -p 8000:8000 --rm -it token uv run src/manage.py runserver 0.0.0.0:8000

docker-compose up

docker compose run --rm app sh -c "uv run src/manage.py makemigrations"
docker compose run --rm app sh -c "uv run src/manage.py migrate"

docker compose run --rm app sh -c "cd src; uv run manage.py test"
