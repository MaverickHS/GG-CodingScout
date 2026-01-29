import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Build client so connections can be re-used across
# requests. This only needs to happen once per session.
client = requests.Session()

BASETEN_API_KEY = os.getenv('BASETEN_API_KEY')

resp = client.post(
    "https://model-4w5gj0p3.api.baseten.co/development/predict",
    headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
    json="My internet is not working properly",
)

print(resp.json())