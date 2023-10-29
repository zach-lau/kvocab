from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["https://www.viki.com/*", "https://www.netflix.com/*"])

@app.get("/")
def handle():
    print("Got a request!")
    return "<p>Hello world!<p>"

def getFilename(movieName : str, ep : str):
    name = movieName.lower().replace(" ", "-")
    return f'data/{name}-{ep}.vtt'

@app.post("/")
def handle_post():
    print("Got post request")
    movieObj = request.json
    vttRes = requests.get(movieObj['url'])
    print(vttRes.json)
    filename = getFilename(movieObj["movieName"], movieObj["ep"])
    with open(filename, "wb") as f:
        f.write(vttRes.content)
    return {"status" : "ok"} 
