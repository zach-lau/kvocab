from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["https://www.viki.com/*", "https://www.netflix.com/*"])

@app.get("/")
def handle():
    print("Got a request!")
    return "<p>Hello world!<p>"

def getFilename(movieName : str, ep : str, content_type : str):
    """ filetype - http filetype """
    # Get name part
    name = movieName.lower().replace(" ", "-")
    print("Got", content_type)

    # Get extension
    if content_type == "text/xml":
        ext = "xml"
    elif content_type == "text/vtt":
        ext = "vtt"
    else:
        ext = "txt"

    return f'data/{name}-{ep}.{ext}'

@app.post("/")
def handle_post():
    print("Got post request")
    movieObj = request.json
    vttRes = requests.get(movieObj['url'])
    filename = getFilename(movieObj["movieName"], movieObj["ep"], vttRes.headers['content-type'])
    with open(filename, "wb") as f:
        f.write(vttRes.content)
    return {"status" : "ok"} 
