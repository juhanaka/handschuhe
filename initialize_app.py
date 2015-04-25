from os import listdir
from os.path import isfile, join
from PIL import Image
from contextlib import closing
import app_config
from labeling_app import connect_db

from labeling_app import connect_db


def fill_db(image_dir):
    filenames = [ fname for fname in listdir(image_dir) if isfile(join(image_dir, fname))]
    sizes = []
    for fname in filenames:
        img = Image.open(join(image_dir, fname))
        sizes.append(','.join(map(str, img.size)))
    n_features = len(app_config.VARIABLE_COLUMNS)
    query_attributes = [[None, fname, sizes[i], False] + [None for i in range(n_features)] for i, fname in enumerate(filenames)]
    conn = connect_db()
    cur = conn.cursor()
    question_marks = ','.join(['?' for _ in query_attributes[0]])
    cur.executemany('INSERT INTO images VALUES ({0})'.format(question_marks), query_attributes)
    conn.commit()
    conn.close()

def resize_images(img_dir, resized_dir, maxwidth):
    filenames = [ fname for fname in listdir(img_dir) if isfile(join(img_dir, fname))]
    for fname in filenames:
        img = Image.open(join(img_dir, fname))
        width, height = img.size
        w_to_h_ratio = width / float(height)
        resized_img = img.resize((maxwidth, int(maxwidth / w_to_h_ratio)))
        resized_img.save(join(resized_dir, fname))

def generate_schema():
    columns_sql = [' '.join(column) for column in app_config.FIXED_COLUMNS + app_config.VARIABLE_COLUMNS]
    return app_config.SCHEMA_SKELETON.format(',\n'.join(columns_sql))

def init_db():
    with closing(connect_db()) as db:
        db.cursor().executescript(generate_schema())
        db.commit()


init_db()
resize_images(app_config.IMAGE_DIR,
              app_config.RESIZE_DIR,
              app_config.IMG_MAXWIDTH)
fill_db(app_config.IMAGE_DIR)


