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

IMG_MAXWIDTH= 1200
NUMBER_OF_LANDMARK_FEATURES = 28

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
           ('all_faces_bounding_box', 'text'),
           ('landmark_features', 'text')]

MULTIPLE_CHOICE_COLUMNS = [('orientation', 'text')]

MULTIPLE_CHOICE_CHOICES = {'orientation': ['straight',
                                           'slight_left',
                                           'slight_right',
                                           'full_left',
                                           'full_right']}

SCHEMA_SKELETON = """drop table if exists images;
                     create table images (
                        {0}
                     );"""
