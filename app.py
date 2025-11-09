from flask import Flask, request,jsonify
from myApp import generate_fake_data

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
    x = generate_fake_data(data, int(number))
    return jsonify(x)
#hello again, the 5th time - testing webhook
if __name__ == "__main__":
    app.run(host='0.0.0.0')
