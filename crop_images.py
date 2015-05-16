import os
import sqlite3
from labeling_app import connect_db
from app_config import IMAGE_DIR, VARIABLE_COLUMNS
from PIL import Image

bbox_features = [feature[0] for feature in VARIABLE_COLUMNS if feature[0].endswith('bounding_box')]
dirs = ['results/' + feature for feature in bbox_features] + ['results/negative_samples']

for dirname in ['results'] + dirs:
    if not os.path.exists(dirname):
        os.makedirs(dirname)

db = connect_db()
cur = db.cursor()
rows = cur.execute('select * from images where labeled=1').fetchall()

def create_negative_samples(img, positive_rectangle):
    minx, miny, maxx, maxy = positive_rectangle
    width, height = img.size
    negative_samples = []
    left_block = [0,0,minx,height]
    right_block = [maxx,0,width,height]
    top_block = [minx,0,maxx,miny]
    bottom_block = [minx,maxy,maxx,height]

    for dims in [left_block,right_block,top_block,bottom_block]:
        negative_samples.append(img.crop(dims))
    return negative_samples

for row in rows:
    fname = row['filename']
    img = Image.open(os.path.join(IMAGE_DIR,fname))
    for i, feature in enumerate(bbox_features):
        feature_coordinates = row[feature]
        cropped_img = img.crop(map(int, feature_coordinates.split(',')))
        cropped_img.save(os.path.join(dirs[i], fname))
    negative_samples = create_negative_samples(img, map(int,row['all_faces_bounding_box'].split(',')))
    for i,sample in enumerate(negative_samples):
        sample.save(os.path.join('results/negative_samples',str(i)+fname))


