"""
Includes handlers to register files with the database
"""

import psycopg2
from configparser import ConfigParser
import csv
import os

def config(filename='database.ini', section='postgresql'):
    """Parse a config file and return a dictionary of credentiali values"""
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

class dbConnection:
    """
    Usage specific db connection
    Note any _methods in this class are designed to be executed within a transaction 
    Any public facing methods should be wrapped in transactions which can be done with @transact
    """
    def __init__(self, inifile):
        creds = config(inifile)
        self.conn = psycopg2.connect(**creds)
        self.db_name = creds["database"]
    # decorator for public facing versions
    def transact(db_func):
        """ WARNING: the existing function needs to take the cursor as an argument but the public faing version wont
        use that """
        def new_func(self, *args, **kwargs):
            with self.conn:
                with self.conn.cursor() as curs:
                    return db_func(self, curs, *args, **kwargs)
        return new_func
    # Simple execute statements
    def _execute(self, curs, statement, *args):
        curs.execute(statement, *args)
        return curs.fetchall()
    def execute(self, statement, *args):
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(statement, *args)
                return curs.fetchall()
    def execute_list(self, statements):
        with self.conn:
            res = []
            with self.conn.cursor() as curs:
                for s in statements:
                    curs.execute(s)
                res.append(curs.fetchall())
        return res
    # Table specific functions
    def get_unique_words(self):
        return [x[0] for x in self.execute("""SELECT DISTINCT WORD FROM WORDS;""")]
    def check_exists(self, word, language : int):
        """ Check if a word exists in the db"""
        res = self.execute(f"""SELECT 1 FROM WORDS WHERE word = %s AND lang = %s;""", (word, language))
        return len(res) > 0
    def update_word(self, word, count):
        """Deprecated - neds updating for POS 
        Update the count of a single word in the db. Add it if it doesn't yet exist"""
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(f"""SELECT WORD, NUM FROM WORDS WHERE word = %s;""", (word,))
                res = curs.fetchall()
                if len(res) > 0:
                    _, old_count = res[0]
                    new_count = old_count + count
                    curs.execute(f"""UPDATE WORDS SET num = %s WHERE word = %s RETURNING *;""", (new_count, word))
                else: # In this case we need a insert
                    curs.execute(f"""INSERT INTO WORDS (word, num) values (%s, %s) RETURNING *;""", (word, count))
                res = curs.fetchall()
        return res
    
    # Private helper functions
    def _check_source_dict(self, curs, word : str, language : int):
        """ Check the source dictionary for if a value exists (not the cached value in the table)"""
        # Dictionary of table names for the dictionaries and check columns
        lang_dicts = {
            1 : ('korean_dictionary','fullform')
        }
        if language not in lang_dicts:
            return False
        target_dict, target_col = lang_dicts[language]
        res = self._execute(curs, f"""SELECT 1 FROM {target_dict} WHERE {target_col} = %s limit 1;""", (word,))
        return len(res) > 0

    def _update_word_list(self, word_list, language : int):
        """ Private method. Update the word count of a list of words (unique on word) in the db. Need to acquire conn 
         before using """
        with self.conn.cursor() as curs:
            # Prep work to get all the words currently in the table
            curs.execute(f"""SELECT WORD, POS, NUM FROM WORDS;""")
            res = curs.fetchall()
            current_dict = {}
            for row in res:
                word, pos, num = row
                key = (word, pos)
                current_dict[key] = num

            # Get a list of "old" words we already have in anki
            curs.execute(f"""SELECT WORD FROM OLD_WORDS""")
            res = curs.fetchall()
            old_set = set([x[0] for x in res])

            # This is where we sort the rows into update vs insert
            update_list = []
            insert_list = []
            for row in word_list:
                word, pos, ex, num = row
                key = (word, pos)
                if key in current_dict.keys():
                    update_list.append(row)
                else: # New word
                    insert_list.append(row) # 4 elements
            # print(update_list)
            # print(insert_list)
            update_sql = f"""UPDATE WORDS SET num = %s WHERE word = %s AND pos = %s;"""
            insert_sql = f"""INSERT INTO WORDS (WORD, POS, EXAMPLE, TYPE, NUM, LANG, IN_DICT) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            def update_tuple(row):
                """ Create an approriate update tuple from a row """
                word, pos, num, ex = row
                old_num = current_dict[(word, pos)]
                num = old_num + int(num)
                return (num, word, pos)
            def insert_tuple(row):
                """Create an appropriate sql insert tuple from row"""
                word, pos, num, ex = row
                # Get type
                if word in old_set:
                    type = 1 # OLD
                else:
                    type = 2 # NEW
                # Check if in the dictionary
                in_dict = self._check_source_dict(curs, word, language)
                return (word, pos, ex, type, num, language, in_dict)
            curs.executemany(update_sql, map(update_tuple, update_list))
            curs.executemany(insert_sql, map(insert_tuple, insert_list))

    def update_many(self, word_list, language : int):
        with self.conn:
            self._update_word_list(self, word_list, language)

    def _file_exists(self, curs, filename : str) -> bool:
        """ Check if a file has been uploaded to the db """
        curs.execute(f"""SELECT FILENAME FROM UPLOADED_FILES WHERE FILENAME = %s;""", (filename,))
        res = curs.fetchall()
        return len(res) > 0
    
    @transact
    def file_exists(self, curs, filename : str) -> bool:
        return self._file_exists(curs, filename)

    def import_file(self, filename, language : int):
        data = []
        with open(filename, 'r') as f:
            r = csv.reader(f)
            data = list(r)
        with self.conn:
            # Check if the file has already been uploaded 
            basename = os.path.basename(filename)
            with self.conn.cursor() as curs:
                if self._file_exists(curs, basename):
                    print(f"The file {basename} has already been uploaded")
                    return
                # Add to files
                curs.execute(f"""INSERT INTO UPLOADED_FILES (FILENAME) VALUES(%s);""", (basename,))
            self._update_word_list(data, language)

    def get_new(self, language : int):
        """Get the most common new word from the database"""
        required_fields = [
            "id", "word", "pos", "meaning", "example", "type", "num", "lang"
        ]
        with self.conn:
            with self.conn.cursor() as curs:
                cols = ','.join(required_fields)
                # Since we control cols we aren't at risk of sql injection
                exec_template = f"""SELECT {cols} FROM WORDS """\
                                f"""WHERE TYPE = 2 AND LANG = %s """\
                                f"""ORDER BY IN_DICT DESC, NUM DESC LIMIT 1;"""
                print(exec_template)
                curs.execute(exec_template, (language,))
                res = curs.fetchone()
                print(res)
        if not res:
            return { "valid" : 0 }
        id, word, pos, meaning, example, type, num, lang = res
        return {
            "valid" : 1,
            "id" : id,
            "word" : word,
            "pos" : pos,
            "meaning" : meaning,
            "example" : example,
            "type" : type,
            "num" : num,
            "lang" : lang
        }
    
    def add_meaning_and_type(self, id, meaning, type):
        """ Add a meaning and update the type for a given word"""
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(f"""UPDATE WORDS SET meaning = %s, type = %s WHERE id = %s""", (meaning, type, id))
        
    def close(self):
        self.conn.close()
    
    def add_alternate(self, word, pos, meaning, type, num, language : int, example=''):
        """ When we add an alternate definition for a word"""
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(f"""INSERT INTO WORDS 
                    (word, pos, meaning, type, num, language, example)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                    ;""", (word, pos, meaning, type, num, language, example))

    def get_types(self):
        """ Return list of tuples of types """
        types = self.execute(f"""SELECT ID, NAME FROM TYPES;""")
        return types
    
    def get_languages(self):
        """ Return list of ids and languages """
        langs = self.execute("SELECT ID, CODE FROM LANGUAGES;")
        return langs
    
    def get_db_name(self):
        """ Get db name """
        return self.db_name

    @transact
    def check_source_dict(self, curs, word : str, language : int):
        return self._check_source_dict(curs, word, language)

if __name__ == '__main__':
    db = dbConnection('database.ini')
    try:
        # res = db.execute('SELECT * FROM WORDS;')
        # res = db.execute_list([
        #     """SELECT * FROM WORDS WHERE word = '학생';""",
        #     """SELECT * FROM WORDS WHERE word = '엄마';"""
        # ])
        # res = db.check_exists('개새끼')A
        # res = db.update_word('졍국 사랑해', 100)
        # db.update_many([
        #     ('정국', 'Noun', 1, ''), 
        #     ('지민', 'Noun', 10, '지민을 사랑한다'),
        #     ('학생', 'Noun', 1, '난 학생이애요')
        #     ])
        # db.import_file('./data/mlfts14.csv')
        # print(db.get_new())
        # db.add_meaning_and_type(10306, "Number one bts member", 7)
        # print(db.get_types())
        # print(db.check_exists('개새끼', 1))
        # print(db.get_languages())
        # print(db.check_source_dict('개', 1))
        print(db.get_new(1))
        # print(res)
    finally:
        db.close()
    