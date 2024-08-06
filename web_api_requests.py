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
