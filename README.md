This is a small project to construct web api with django

it is based on udemy course
Create an advanced REST API with Python, Django REST Framework and Docker using Test Driven Development (TDD)

### Docker commands

    docker build -t <repo>:<tag> .
    docker images
    docker container ls -a
    docker run --rm -it <image> <command>
    docker exec -it <container> <command>

### Docker compose commands

    docker-compose run --rm app
    docker-compose run --rm app sh
    docker-compose run --rm app sh -c <command>
    docker-compose up
    docker-compose build
    docker-compose -f <compose file> <params>

### Django commands

    docker-compose run --rm app sh -c "django-admin startproject <name> ."
    docker-compose run --rm app sh -c "python manage.py test"
    docker-compose run --rm app sh -c flake8
    docker-compose run --rm app sh -c "python manage.py startapp <name>"
    docker-compose run --rm app sh -c "python manage.py wait_for_db"
    docker-compose run --rm app sh -c "python manage.py migrate"
    docker-compose run --rm app sh -c "python manage.py makemigrations"
    docker-compose run --rm app sh -c "python manage.py createsuperuser"
    docker-compose run --rm app sh -c "python manage.py makemessages -l <lang>"
    docker-compose run --rm app sh -c "python manage.py compilemessages"
    docker-compose run --rm app sh -c "python manage.py collectstatic"
