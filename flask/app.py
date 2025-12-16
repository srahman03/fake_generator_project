from flask import Flask, request,jsonify, Response
from myApp import generate_fake_data
import json
import hashlib
app = Flask(__name__)

@app.get("/api/schema")
def get_schema():
    body = request.json
    return body

@app.get("/api/schema/count")
def get_count():
    body = request.json
    return str(body["count"])

@app.post("/api/schema")
def add_schema():
    data = request.get_json()
    count =  request.args.get('count',default=1)
    result = generate_fake_data(data, int(count))
    accept = request.headers.get("Accept")
    index_name = "f1_index_2"
    lines=[]
    lines_for_ndjson = []
    for i in result:
        doc_id = hashlib.sha256(json.dumps(i, sort_keys=True).encode()).hexdigest()
        lines.append(json.dumps({"index": {"_index": index_name, "_id": doc_id}}))
        lines.append(json.dumps(i))
        lines_for_ndjson.append(json.dumps(i))
    bulk_api_str = "\n".join(lines) + "\n"

    with open('file.txt', "w") as f:
        f.write(bulk_api_str)

    if "application/x-ndjson" in accept:
        ndjson_str = "\n".join(lines_for_ndjson) + "\n"

        return Response(
            ndjson_str,
            mimetype="application/x-ndjson"
        )
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
