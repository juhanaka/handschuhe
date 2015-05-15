import os
import sqlite3
from labeling_app import connect_db
from app_config import IMAGE_DIR, VARIABLE_COLUMNS
from PIL import Image

bbox_features = [feature[0] for feature in VARIABLE_COLUMNS if feature[0].endswith('bounding_box')]
dirs = ['results/' + feature for feature in bbox_features]

for dirname in ['results'] + dirs:
    if not os.path.exists(dirname):
        os.makedirs(dirname)

db = connect_db()
cur = db.cursor()
rows = cur.execute('select * from images where labeled=1').fetchall()

for row in rows:
    fname = row['filename']
    img = Image.open(os.path.join(IMAGE_DIR,fname))
    for i, feature in enumerate(bbox_features):
        feature_coordinates = row[feature]
        cropped_img = img.crop(map(int, feature_coordinates.split(',')))
        cropped_img.save(os.path.join(dirs[i], fname))
