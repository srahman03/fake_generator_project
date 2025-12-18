from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import requests
import os
from dotenv import load_dotenv

schema_data = {
    "wins": {"type":"int","min":0,"max":100},
    "name": {"type":"name"},
    "username":{"type":"username"},
    "driver":{"type":"driver"},
    "ip_address": {"type":"ip"},
    "distance_of_track":{"type":"distance"},
    "date_of_race":{"type":"date"},
    "podiums_for_driver":{"type":"int","min":0,"max":250},
    "latitude":{"type":"latitude"},
    "longitude":{"type":"longitude"},
    "circuit":{"type":"circuit"},
    "date_of_birth":{"type":"dob"},
    "text":{"type":"text"},
    "team_for_driver":{"type":"team"},
    "tyres":{"type":"tyres"},
    "weather":{"type":"weather"},
    "logs":"log"
}

def create_index(client):
    pipeline_body = {
        "description": "my index parser",
        "processors": [
            {
                "grok": {
                    "field": "logs",
                    "patterns": [
                        "%{DAY:log.day} %{MONTH:log.month} %{MONTHDAY:log.month-day} %{TIMESTAMP_ISO8601:log.timestamp} %{IP:log.ip} %{WORD:log.my_word} %{NUMBER:log.http_code} %{GREEDYDATA:log.log_line}"
                    ]
                }
            },
            {
                "geoip": {
                    "field": "log.ip",
                    "target_field": "geoip"
                }
            }
        ]
    }
    # Create the pipeline
    client.ingest.put_pipeline(id="my_pipeline", body=pipeline_body)

    mapping = {
        "settings": {"number_of_shards": 1},
        "mappings": {
            "properties": {
                "geoip": {
                    "properties": {
                        "location": {"type": "geo_point"}
                    }
                }
            }
        },
    }
    client.indices.create(index="my_f1_index", body=mapping, ignore=400)

def generate_actions(flask_url,params,headers):

    for _ in range(1, 10):
        response = requests.post(
            flask_url,
            params=params,
            json=schema_data,
            headers=headers
        )

        if headers["Accept"] == "application/x-ndjson":
            for c in response.iter_lines():
                yield {
                    "_index": "my_f1_index",
                    "_source": c,
                    "pipeline": "my_pipeline"
                }
        else:
            for doc in response.json():
                yield {
                    "_index": "my_f1_index",
                    "_source": doc,
                    "pipeline": "my_pipeline"
                }

def main():
    print("Downloading dataset...")
    load_dotenv()
    client = Elasticsearch(
        'https://elastic-latest.netbuilder-training.com',
        basic_auth=("elastic", os.getenv("PASS")))
    print("Creating index...")
    create_index(client)

    #Sending to elastic api
    flask_url = "https://flask-app-sr.netbuilder-training.com/api/schema"
    params = {"count": 10}
    headers = {"Accept": "application/json"}
    print("Indexing documents...")
    successes = 0
    for ok, _ in streaming_bulk(client, index="my_f1_index", actions=generate_actions(flask_url,params,headers)):
        successes += ok
    print(f"Indexed {successes} documents")


if __name__ == "__main__":
    main()
