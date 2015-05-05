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

VARIABLE_COLUMNS = [('face_bounding_box', 'text'),
           ('left_eye_bounding_box', 'text'),
           ('right_eye_bounding_box', 'text'),
           ('mouth_bounding_box', 'text'),
           ('nose_bounding_box', 'text'),
           ('landmark_features', 'text')]

SCHEMA_SKELETON = """drop table if exists images;
                     create table images (
                        {0}
                     );"""
