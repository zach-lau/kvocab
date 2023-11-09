"""
A worker script which is able to process a subtitle file and upload it to the appropriate database
database.ini has to be in the path
"""

from kvocab.database import dbConnection
import logging
from kvocab.digest import digest
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def process_file(filename : str, language : int, dbfile = "database.ini"):
    try:
        outfile = digest(filename, language)
    except Exception as e:
        logging.info(f"Problem extracting outfile: {e}")
     
    try:
        db = dbConnection(dbfile)
    except Exception as e:
        logging.info("Failed to connect to db")
        logging.debug(e) 
        return
    
    try:
        db.import_file(outfile, language)
    except Exception as e:
        logging.debug(f"Database error {e}")
    finally:
        if db:
            db.close()
    logging.info(f"Successully updated file {filename}")
