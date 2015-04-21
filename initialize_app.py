from labeling_app import init_db
from fill_db_from_folder import fill_db
from app_config import IMAGE_DIR

init_db()
fill_db(IMAGE_DIR)


