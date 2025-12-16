import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = "https://elastic-latest.netbuilder-training.com/_bulk"

headers = {"Content-Type": "application/x-ndjson"}

with open("/data/file.txt", "rb") as f:
    data = f.read()

response = requests.post(
    url,
    headers=headers,
    data=data,
    auth=("elastic", os.getenv("PASS"))
)

print(response.text)

