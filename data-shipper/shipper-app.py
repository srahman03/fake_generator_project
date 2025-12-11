import requests

url = "https://elastic-latest.netbuilder-training.com/_bulk"
headers = {"Content-Type": "application/x-ndjson"}

with open("flask/file.txt", "rb") as f:
    data = f.read()

response = requests.post(
    url,
    headers=headers,
    data=data,
    auth=("elastic", "bCDNi5NtUSBuTmYgE0vvS6uZ")
)

print(response.text)

