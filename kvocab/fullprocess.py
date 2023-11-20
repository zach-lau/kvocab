"""
A worker script which is able to process a subtitle file and upload it to the appropriate database
database.ini has to be in the path
"""

from kvocab.database import dbConnection
import logging
from kvocab.digest import digest
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def get_outfile_name(infile):
    """ Get the output file name so we can check if it already exists in the db """
    basename = os.path.basename(infile)
    root, _ = os.path.splitext(basename)
    return f"{root}.csv"

def process_file(filename : str, language : int, dbfile = "database.ini"):

    db_access = False
    try:
        db = dbConnection(dbfile)
        db_access = True
        logging.info("Connected to db") 
    except Exception as e:
        logging.info("Failed to connect to db")
        logging.debug(e) 
    
    outfile = get_outfile_name(filename)
    if db.file_exists(outfile):
        logging.info("Outfile already exists, skipping processing")
        return

    try:
        outfile = digest(filename, language)
        logging.info(f"Wrote out file {filename}")
    except Exception as e:
        logging.info(f"Problem extracting outfile: {e}")
        return 

    if db_access: 
        try:
            db.import_file(outfile, language)
            logging.info(f"Successully updated file {filename}")
        except Exception as e:
            logging.info(f"Failed to upload file {filename}")
            logging.debug(f"Database error {e}")
        finally:
            if db:
                db.close()
