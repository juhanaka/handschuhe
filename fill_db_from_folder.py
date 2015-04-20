from os import listdir
from os.path import isfile, join
from labeling_app import connect_db

IMAGE_DIR = 'static/images'

filenames = [ fname for fname in listdir(IMAGE_DIR) if isfile(join(IMAGE_DIR, fname))]
query_attributes = [(None, fname, 0, 'NULL', 'NULL') for fname in filenames]

conn = connect_db()
cur = conn.cursor()

cur.executemany('INSERT INTO images VALUES (?,?,?,?,?)', query_attributes)
conn.commit()
conn.close()


