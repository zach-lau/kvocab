from flask import Flask, request
import requests

app = Flask(__name__)

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
