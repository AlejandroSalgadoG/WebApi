This a small project to construct web api with django

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
