import os
import sqlite3
from labeling_app import connect_db
from app_config import IMAGE_DIR, VARIABLE_COLUMNS
from PIL import Image


bbox_features = [feature[0] for feature in VARIABLE_COLUMNS if feature[0].endswith('bounding_box')]

if not os.path.exists('results'):
    os.makedirs('results')

bbox_files = {}

for feature in bbox_features:
    fp = open('results/bbox_file_{0}'.format(feature), 'a')
    bbox_files[feature] = fp

db = connect_db()
cur = db.cursor()
rows = cur.execute('select * from images where labeled=1').fetchall()

for row in rows:
    fname = row['filename']
    for i, feature in enumerate(bbox_features):
        feature_coords = map(int, row[feature].split(','))
        formatted_coords = map(str,[feature_coords[0], feature_coords[1],
                            feature_coords[2]-feature_coords[0],
                            feature_coords[3]-feature_coords[1]])
        bbox_files[feature].write('img/{0}  1  {1}\n'.format(fname, ' '.join(formatted_coords)))


