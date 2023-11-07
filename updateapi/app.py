from flask import Flask, request
from kvocab.database import dbConnection

# Decorator for db accessing functions
def db_safe_func(func):
    def ret_func():
        try:
            db = dbConnection("../database.ini")
            return func(db)
        except Exception as e:
            print(e)
            return { "status" : "Fail" }
        finally:
            db.close()
    return ret_func
app = Flask(__name__)

@app.get("/new")
def get_next_word():
    try:
        db = dbConnection("../database.ini")
        language = int(request.args.get('language'))
        return db.get_new(language)
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

@app.post("/addnew")
def add_new():
    try:
        db = dbConnection("../database.ini")
        vals = request.json
        if db.check_exists(vals["word"], vals["language"]):
            return {"status":"Fail", "reason":"Already exists"}
        db.add_alternate(
            vals["word"],
            vals["pos"],
            vals["meaning"],
            vals["type"],
            vals["num"],
            vals["language"],
            vals["example"],
        )
    except Exception as e:
        print(e)
        return { "status" : "Fail" } 
    finally:
        db.close()

@app.get("/types")
def get_types():
    try:
        db = dbConnection("../database.ini")
        types = db.get_types()
        return {
            "types" : [{"id":x[0], "value":x[1]} for x in types]
        }
        
    except Exception as e:
        print(e)
        return { "status" : "Fail" }
    finally:
        db.close()
        
@app.get("/languages")
def get_languages():
    try:
        db = dbConnection("../database.ini")
        langs = db.get_languages()
        return {
            "languages" : [{"id":id,"value":code} for id, code in langs]
        }
    except Exception as e:
        print(e)
        return { "status" : "Fail" }
    finally:
        db.close()

@app.get("/dbname")
@db_safe_func
def get_dbname(db : dbConnection):
    return { "name" : db.get_db_name()}
