import logging
import requests

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
)

SERVER_URL = 'http://localhost:8000'
EMAIL = "request@example.com"
NAME = "request user"
PASSWORD = "test123"


################### create user ###################
logging.info("start creation of new user")
payload = {
    "email": EMAIL,
    "password": PASSWORD,
    "name": NAME,
}
response = requests.post(f"{SERVER_URL}/api/user/create/", json=payload)
content = response.json()

assert response.status_code == 201
assert len(content) == 2
assert content["email"] == EMAIL
assert content["name"] == NAME
logging.info("new user created")
