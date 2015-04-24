from os import listdir
from os.path import isfile, join
from PIL import Image
from labeling_app import init_db, connect_db
from app_config import IMAGE_DIR, RESIZE_DIR, IMG_MAXWIDTH
from labeling_app import connect_db


def fill_db(image_dir):
    filenames = [ fname for fname in listdir(image_dir) if isfile(join(image_dir, fname))]
    sizes = []
    for fname in filenames:
        img = Image.open(join(image_dir, fname))
        sizes.append(','.join(map(str, img.size)))
    query_attributes = [(None, fname, sizes[i], None, None, None, None) for i, fname in enumerate(filenames)]
    conn = connect_db()
    cur = conn.cursor()
    cur.executemany('INSERT INTO images VALUES (?,?,?,?,?,?,?)', query_attributes)
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



init_db()
resize_images(IMAGE_DIR, RESIZE_DIR, IMG_MAXWIDTH)
fill_db(IMAGE_DIR)


