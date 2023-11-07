#!/usr/bin/env python3

from kvocab.database import dbConnection
import sys
import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog = 'digest',
        description = 'Process subtite file and produce sorted list of morphemes',
    )
    parser.add_argument(
        "language",
        choices = ['ko','yue'],
    )
    parser.add_argument(
        'files',
        nargs=argparse.REMAINDER
    )
    args = parser.parse_args()
    dir_path = os.path.dirname(os.path.realpath(__file__)) # Ugly hack to import db
    # Hard code this here... can update witih database later
    code_dict = {
        "ko" : 1,
        "yue" : 2,
        "ja" : 3
    }
    lang_code = code_dict[args.language]
    db = dbConnection(f"{dir_path}/database.ini")
    for file in args.files:
        try:
            db.import_file(file, lang_code)
            print(f"Processed {file}")
        except:
            print(f"Problem importing {file}")
    db.close()
            