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

TITLE = "test title"
MINUTES = 5
PRICE = "5.43"
LINK = "http://www.example.com"
DESCRIPTION = "test description"


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

################### create token ###################
logging.info("start creation of new user token")
response = requests.post(f"{SERVER_URL}/api/user/token/", json=payload)
content = response.json()

assert response.status_code == 200
assert len(content) == 1
assert "token" in content

token = content["token"]

logging.info(f"user token created: {token}")

################### consult user ###################
logging.info("consulting user information")
response = requests.get(f"{SERVER_URL}/api/user/me", headers={'Authorization': f'Token {token}'})
content = response.json()

assert response.status_code == 200
assert len(content) == 2
assert content["email"] == EMAIL
assert content["name"] == NAME
logging.info("new user consulted")

################### create recipe ###################
logging.info("start creation of recipie")
payload = {
  "title": TITLE,
  "time_minutes": MINUTES,
  "price": PRICE,
  "link": LINK,
  "description": DESCRIPTION,
}
response = requests.post(f"{SERVER_URL}/api/recipe/recipes/", headers={'Authorization': f'Token {token}'}, json=payload)
content = response.json()

assert response.status_code == 201
assert len(content) == 6
assert "id" in content
assert content["title"] == TITLE
assert content["time_minutes"] == MINUTES
assert content["price"] == PRICE
assert content["link"] == LINK
assert content["description"] == DESCRIPTION

logging.info("new recipe created")
