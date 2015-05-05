import os
import sqlite3
from labeling_app import connect_db
from app_config import IMAGE_DIR
from PIL import Image

dirs = {'base': 'results', 'faces':'results/faces',
        'lefteyes': 'results/lefteyes', 'righteyes': 'results/righteyes',
        'mouths': 'results/mouths',
        'noses': 'results/noses'}

for (k, d) in dirs.items():
    if not os.path.exists(d):
        os.makedirs(d)

db = connect_db()
cur = db.cursor()
rows = cur.execute('select * from images').fetchall()

for row in rows:
    id_ = row['id']
    fname = row['filename']
    f_coord = row['face_bounding_box']
    le_coord = row['left_eye_bounding_box']
    re_coord = row['right_eye_bounding_box']
    m_coord = row['mouth_bounding_box']
    n_coord = row['nose_bounding_box']

    img = Image.open(os.path.join(IMAGE_DIR,fname))
    face = img.crop(map(int,f_coord.split(',')))
    lefteye = img.crop(map(int,le_coord.split(',')))
    righteye = img.crop(map(int,re_coord.split(',')))
    mouth = img.crop(map(int,m_coord.split(',')))
    nose = img.crop(map(int,n_coord.split(',')))
    face.save(os.path.join(dirs['faces'],fname))
    lefteye.save(os.path.join(dirs['lefteyes'],fname))
    righteye.save(os.path.join(dirs['righteyes'],fname))
    mouth.save(os.path.join(dirs['mouths'],fname))
    nose.save(os.path.join(dirs['noses'],fname))


