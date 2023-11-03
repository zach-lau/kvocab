from flask import Flask, request
from database import dbConnection

app = Flask(__name__)

@app.get("/new")
def get_next_word():
    try:
        db = dbConnection("../database.ini")
        return db.get_new()
    except Exception as e:
        print(e)
        return { "status" : "Fail" }
    finally:
        db.close()

@app.post("/update")
def add_meaning():
    try:
        db = dbConnection("../database.ini")
        vals = request.json
        # Check that we have the keys we need
        for key in ["id", "meaning", "type"]:
            if not key in vals.keys():
                return { "status" : "Fail", "reason": "Invalid information"}
        db.add_meaning_and_type(vals["id"], vals["meaning"], vals["type"])
        return { "status" : "Ok" }
    except Exception as e:
        print(e)
        return { "status" : "Fail" }
    finally:
        db.close()

@app.get("/types")
def get_types():
    try:
        db = dbConnection("../database.ini")
        return db.get_types()
    except Exception as e:
        print(e)
        return { "status" : "Fail" }
    finally:
        db.close()
        