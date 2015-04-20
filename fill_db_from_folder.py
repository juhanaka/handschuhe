from os import listdir
from os.path import isfile, join
from labeling_app import connect_db

def fill_db(image_dir):
    filenames = [ fname for fname in listdir(image_dir) if isfile(join(image_dir, fname))]
    query_attributes = [(None, fname, None, None, None, None) for fname in filenames]
    conn = connect_db()
    cur = conn.cursor()
    cur.executemany('INSERT INTO images VALUES (?,?,?,?,?,?)', query_attributes)
    conn.commit()
    conn.close()


