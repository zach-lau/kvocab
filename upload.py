#!/usr/bin/env python3

from database import dbConnection
import sys
import os


if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db = dbConnection(f"{dir_path}/database.ini")
    for file in sys.argv[1:]:
        try:
            db.import_file(file)
            print(f"Processed {file}")
        except:
            print(f"Problem importing {file}")
    db.close()
            