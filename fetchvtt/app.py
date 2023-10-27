from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["https://www.viki.com/*"])

@app.get("/")
def handle():
    print("Got a request!")
    return "<p>Hello world!<p>"

@app.post("/")
def handle_post():
    print("Got post request")
    movieObj = request.json
    vttRes = requests.get(movieObj['url'])
    print(vttRes.json)
    with open("outfile.vtt", "wb") as f:
        f.write(vttRes.content)
    return {"status" : "ok"} 
