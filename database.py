"""
Includes handlers to register files with the database
"""

import psycopg2
from configparser import ConfigParser
import csv

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
    """
    def __init__(self, inifile):
        creds = config(inifile)
        self.conn = psycopg2.connect(**creds)
    def execute(self, statement):
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(statement)
                return curs.fetchall()
    def execute_list(self, statements):
        with self.conn:
            res = []
            with self.conn.cursor() as curs:
                for s in statements:
                    curs.execute(s)
                res.append(curs.fetchall())
        return res
    def get_unique_words(self):
        return [x[0] for x in self.execute("""SELECT DISTINCT WORD FROM WORDS;""")]
    def check_exists(self, word):
        """ Check if a word exists in the db"""
        res = self.execute(f"""SELECT 1 FROM WORDS WHERE word = '{word}';""")
        return len(res) > 0
    def update_word(self, word, count):
        """Deprecated - neds updating for POS 
        Update the count of a single word in the db. Add it if it doesn't yet exist"""
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute(f"""SELECT WORD, NUM FROM WORDS WHERE word = '{word}';""")
                res = curs.fetchall()
                if len(res) > 0:
                    _, old_count = res[0]
                    new_count = old_count + count
                    curs.execute(f"""UPDATE WORDS SET num = {new_count} WHERE word = '{word}' RETURNING *;""")
                else: # In this case we need a insert
                    curs.execute(f"""INSERT INTO WORDS (word, num) values ('{word}', {count}) RETURNING *;""")
                res = curs.fetchall()
        return res
    def update_many(self, word_list):
        """ Update the word count of a list of words (unique on word) in the db """
        with self.conn:
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
                insert_sql = f"""INSERT INTO WORDS (WORD, POS, EXAMPLE, TYPE, NUM) 
                                 VALUES (%s, %s, %s, %s, %s);"""
                def update_tuple(row):
                    """ Create an approriate update tuple from a row """
                    word, pos, num, ex = row
                    old_num = current_dict[(word, pos)]
                    num += old_num
                    return (num, word, pos)
                def insert_tuple(row):
                    """Create an appropriate sql insert tuple from row"""
                    word, pos, num, ex = row
                    if word in old_set:
                        type = 1 # OLD
                    else:
                        type = 2 # NEW
                    return (word, pos, ex, type, num)
                curs.executemany(update_sql, map(update_tuple, update_list))
                curs.executemany(insert_sql, map(insert_tuple, insert_list))
        
    def import_file(self, filename):
        data = []
        with open(filename, 'r') as f:
            r = csv.reader(f)
            data = list(r)
        self.update_many(data)
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    try:
        db = dbConnection('database.ini')
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
        db.import_file('./data/mlfts14.csv')
        # print(res)
    finally:
        db.close()
    