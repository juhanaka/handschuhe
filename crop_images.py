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

db = sqlite3.connect('labeling_app.db')
cur = db.cursor()
rows = cur.execute('select * from images').fetchall()

for row in rows:
    id_, fname, f_coord, e_coord, m_coord, n_coord = row
    img = Image.open(os.path.join(IMAGE_DIR,fname))
    face = img.crop(map(int,f_coord.split(',')))
    eye_coordinates = map(int,e_coord.split(','))
    lefteye = img.crop(eye_coordinates[0:4])
    righteye = img.crop(eye_coordinates[4:])
    mouth = img.crop(map(int,m_coord.split(',')))
    nose = img.crop(map(int,n_coord.split(',')))
    face.save(os.path.join(dirs['faces'],fname))
    lefteye.save(os.path.join(dirs['lefteyes'],fname))
    righteye.save(os.path.join(dirs['righteyes'],fname))
    mouth.save(os.path.join(dirs['mouths'],fname))
    nose.save(os.path.join(dirs['noses'],fname))


