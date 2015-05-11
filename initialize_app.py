from os import listdir
from os.path import isfile, join
from PIL import Image
from contextlib import closing
import app_config
from labeling_app import connect_db


def fill_db(image_dir):
    filenames = [ fname for fname in listdir(image_dir) if isfile(join(image_dir, fname))]
    sizes = []
    for fname in filenames:
        img = Image.open(join(image_dir, fname))
        sizes.append(','.join(map(str, img.size)))
    n_features = len(app_config.VARIABLE_COLUMNS) + len(app_config.MULTIPLE_CHOICE_COLUMNS)
    query_attributes = [[None, fname, None, sizes[i], False] +
                        [None for i in range(n_features)] for i, fname in enumerate(filenames)]
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
    columns = app_config.FIXED_COLUMNS + app_config.VARIABLE_COLUMNS + app_config.MULTIPLE_CHOICE_COLUMNS
    columns_sql = [' '.join(column) for column in columns]
    return app_config.SCHEMA_SKELETON.format(',\n'.join(columns_sql))

def init_db():
    with closing(connect_db()) as db:
        db.cursor().executescript(generate_schema())
        with open('schema.sql') as fp:
            db.cursor().executescript(fp.read())
        db.commit()

def create_admin():
    with open(app_config.ADMIN_PASSWORD_FILE) as fp:
        admin_pass = fp.read().strip()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""INSERT INTO users VALUES (NULL, 'admin', '{0}')""".format(admin_pass))
    conn.commit()
    conn.close()


init_db()
resize_images(app_config.IMAGE_DIR,
              app_config.RESIZE_DIR,
              app_config.IMG_MAXWIDTH)
fill_db(app_config.IMAGE_DIR)
create_admin()


