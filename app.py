from flask import Flask, request,jsonify, Response
from myApp import generate_fake_data
import json
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
    number = data.get("count", 1)
    result = generate_fake_data(data, int(number))
    accept = request.headers.get("Accept")

    if "application/x-ndjson" in accept:
        index_name = "f1_index"
        lines=[]
        for item in result:
            lines.append(json.dumps({"index": {"_index": index_name}}))
            lines.append(json.dumps(item))
        ndjson_str = "\n".join(lines) + "\n"

        with open('file.txt', "w") as f:
            f.write(ndjson_str)
        return Response(
            ndjson_str,
            mimetype="application/x-ndjson"
        )
    with open('file.txt', "w") as f:
        f.write(result)

    return jsonify(result)

#Testing jenkins pipeline with dockerfile
if __name__ == "__main__":
    app.run(host='0.0.0.0')
