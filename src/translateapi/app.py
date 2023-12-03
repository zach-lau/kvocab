"""Flask app designed as a wrapper for deepl api with api key"""

import requests
from flask import Flask, request
from configparser import ConfigParser


def config(filename='deepl.ini', section='DeepL'):
    """Parse a config file and return a dictionary of credential values"""
    parser = ConfigParser()
    parser.read(filename)
    res = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            key, value = param
            res[key] = value
    else:
        raise Exception(f'Section {section} not found in fie {filename}')
    return res

app = Flask(__name__)
dbsettings = config() # Crash and exit if not present

@app.post("/")
def translate_word():
    # Parse the request
    text = request.json["text"]

    # Get required headers for deepl
    url = dbsettings["hosturl"]
    authtype = dbsettings["authtype"]
    key = dbsettings["key"]
    resp = requests.post(
        url,
        headers = { "Authorization" : f"{authtype} {key}" },
        data = { "target_lang" : "EN", "text" : [text] }
    )
    if not resp.ok:
        return { "status" : "bad" , "reason" : resp.status_code }

    # Parse deepl response
    print(resp.json())
    text = resp.json()["translations"][0]["text"]


    return { "status" : "ok ", "text" : text }
