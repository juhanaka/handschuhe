IMAGE_DIR = 'static/images'
RESIZE_DIR = 'static/resized_images'
ADMIN_PASSWORD_FILE = '../admin_password'
APP_CONFIG = dict(
    DATABASE='/tmp/labeling_app.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
)

IMG_MAXWIDTH= 800
NUMBER_OF_LANDMARK_FEATURES = 7

FIXED_COLUMNS = [('id', 'integer', 'primary key'),
                 ('filename', 'text', 'unique', 'not null'),
                 ('username', 'text'),
                 ('size', 'text'),
                 ('labeled', 'integer')]

VARIABLE_COLUMNS = [('face_coordinates', 'text'),
           ('left_eye_coordinates', 'text'),
           ('right_eye_coordinates', 'text'),
           ('mouth_coordinates', 'text'),
           ('nose_coordinates', 'text'),
           ('landmark_features', 'text')]

SCHEMA_SKELETON = """drop table if exists images;
                     create table images (
                        {0}
                     );"""
