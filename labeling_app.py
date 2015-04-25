import sqlite3
import json
from contextlib import closing
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response
from flask.views import MethodView, View
from app_config import APP_CONFIG, VARIABLE_COLUMNS

# Configuration etc.
#-----------------------------------------
app = Flask(__name__)
app.config.update(APP_CONFIG)
app.debug = True

def check_auth(username, password):
    return username == 'admin' and password == 'default'

def authenticate():
    return Response(
    'You have to log in', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
@requires_auth
def index():
    return redirect(url_for('list_images'))

# Views
#-----------------------------------------

class LabelImageView(MethodView):
    template = 'label_image.html'

    def get_object(self, img_id=None):
        if img_id is None:
            qstring = 'select * from images where face_coordinates is null limit 1'
        else:
            qstring = 'select * from images where id = {0}'.format(img_id)
        cur = g.db.execute(qstring)
        return cur.fetchone()

    def save_coordinates(self, coordinates, filename):
        coordinates_floats = {key: map(float,value.split(',')) for key, value in coordinates.items()}
        coordinates_strings = {key: ','.join(map(str, map(int, value))) for key, value in coordinates_floats.items()}
        coordinates_joined = ['{0}={1}'.format(key, '"' + value + '"') for key, value in coordinates_strings.items()]
        qstring = 'update images set {0}, labeled=1 where filename={1}'.format(','.join(coordinates_joined),
                                                                    '"'+filename+'"')
        print qstring
        g.db.execute(qstring)
        g.db.commit()

    def get_min_and_max_id(self):
        cur = g.db.execute('select min(id), max(id) from images')
        return cur.fetchone()

    def get_coordinates(self, form):
        coordinates = {}
        for col in VARIABLE_COLUMNS:
            key = col[0]
            coordinates[key] = ','.join([form[key + '_ul_x'], form[key + '_ul_y'],
                                         form[key + '_lr_x'], form[key + '_lr_y']])
        return coordinates

    @requires_auth
    def get(self, img_id=None):
        obj = self.get_object(img_id)
        if obj is None:
            return render_template(self.template)

        filename = obj['filename']
        img_id = obj['id']
        img_size = map(int, obj['size'].split(','))
        if obj['labeled']:
            coordinates = {col[0]: map(int, obj[col[0]].split(',')) for col in VARIABLE_COLUMNS}
        else:
            coordinates = {col[0]: None for col in VARIABLE_COLUMNS}
        min_id, max_id = self.get_min_and_max_id()
        prev = img_id - 1 if img_id - 1 >= min_id else None
        next_ = img_id + 1 if img_id + 1 <= max_id else None
        return render_template(self.template, filename=filename,
                               img_size=img_size,
                               coordinates=coordinates,
                               coordinates_json=json.dumps(coordinates),
                               prev=prev, next=next_)

    @requires_auth
    def post(self, img_id=None):
        filename = request.form['filename']
        coordinates = self.get_coordinates(request.form)
        self.save_coordinates(coordinates, filename)
        return self.get()


class ListImagesView(View):
    @requires_auth
    def dispatch_request(self):
        cur = g.db.execute('select * from images')
        q_result = cur.fetchall()
        items = []
        for row in q_result:
            row_dict = {key: row[key] for key in row.keys()}
            items.append(row_dict)
        return render_template('list.html', items=items)


# Routing
#-----------------------------------------
label_image = LabelImageView.as_view('label_image')
list_view = ListImagesView.as_view('list_images')

app.add_url_rule('/image',
                 view_func=label_image)
app.add_url_rule('/image/<img_id>',
                 view_func=label_image)
app.add_url_rule('/list',
                 view_func=list_view)


if __name__ == "__main__":
    app.debug = True
    app.run()
