from flask import Flask, request
from flask_cors import CORS
import requests
import os

# For queuing the file
from rq import Queue
from redis import Redis
from kvocab.fullprocess import process_file
from kvocab.language_mappings import language_mappings

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["https://www.viki.com/*", "https://www.netflix.com/*"])

if "REDIS_HOST" in os.environ:
    REDIS_HOST = os.environ["REDIS_HOST"]
else:
    REDIS_HOST = "localhost"

@app.get("/")
def handle():
    print("Got a request!")
    return "<p>Hello world!<p>"

def getFilename(movie_obj, content_type : str):
    """ filetype - http filetype """
    # Get name part
    movieName = movie_obj["movieName"]
    ep = movie_obj["ep"]
    lang = movie_obj["lang"]

    name = movieName.lower().replace(" ", "-")
    print("Got", content_type)

    # Get extension
    if "text/xml" in content_type:
        ext = "xml"
    elif "text/vtt" in content_type:
        ext = "vtt"
    else:
        ext = "txt"

    dir = f'data/{lang}'
    file = f'{name}-{ep}.{ext}'
    return dir, file 

@app.post("/")
def handle_post():
    print("Got post request")
    movieObj = request.json
    vttRes = requests.get(movieObj['url'])
    dir, file = getFilename(movieObj, vttRes.headers['content-type'])
    if not os.path.isdir(dir):
        os.makedirs(dir)
    filename = os.path.join(dir,file)
    with open(filename, "wb") as f:
        f.write(vttRes.content)
    print(f'Wrote out {filename}')
    try:
        q = Queue(connection=Redis(REDIS_HOST))
        lang = language_mappings[movieObj["lang"]]
        q.enqueue(process_file, filename, lang)
    except Exception as e:
        print("Failed to queue. Upload manually")
        print(e)
    return {"status" : "ok"} 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    