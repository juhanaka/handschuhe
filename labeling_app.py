import os
import sqlite3
import json
from contextlib import closing
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response
from flask.views import MethodView, View
from app_config import (APP_CONFIG, VARIABLE_COLUMNS, NUMBER_OF_LANDMARK_FEATURES)

# Configuration etc.
#-----------------------------------------
app = Flask(__name__)
app.config.update(APP_CONFIG)
app.config.update({'SECRET_KEY': os.urandom(24)})

def check_auth(username, password):
    qstring = """select * from users where username = '{0}'""".format(username)
    cur = g.db.execute(qstring)
    user = cur.fetchone()
    if user is not None:
        return password == user['password']
    return false

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
    return redirect(url_for('label_image'))

# Views
#-----------------------------------------

class LabelImageView(MethodView):
    template = 'label_image.html'

    def get_object(self, username, img_id=None):
        if img_id is None:
            if username != 'admin':
                qstring = """select * from images where labeled=0 and username='{0}'""".format(username)
            else:
                qstring = """select * from images where labeled=0"""
        else:
            qstring = 'select * from images where id = {0}'.format(img_id)
        cur = g.db.execute(qstring)
        return cur.fetchone()

    def save_coordinates(self, coordinates, filename):
        coordinates_joined = []
        for key, value in coordinates.items():
            floats = map(float, value.split(','))
            ints = map(int, floats)
            query_format = '"{0}"'.format(','.join(map(str, ints)))
            coordinates_joined.append('{0}={1}'.format(key, query_format))
        qstring = 'update images set {0}, labeled=1 where filename=?'.format(
            ','.join(coordinates_joined)
        )
        g.db.execute(qstring, (filename,))
        g.db.commit()

    def get_prev_and_next(self, img_id):
        cur = g.db.execute('select min(id), max(id) from images')
        min_id, max_id = cur.fetchone()
        prev = img_id - 1 if img_id - 1 >= min_id else None
        next_ = img_id + 1 if img_id + 1 <= max_id else None
        return prev, next_

    def get_coordinates(self, form):
        coordinates = {}
        for col in VARIABLE_COLUMNS:
            key = col[0]
            if key.startswith('landmark'):
                coordinates[key] = form[key + '_xy']
            else:
                coordinates[key] = ','.join([form[key + '_ul_x'], form[key + '_ul_y'],
                                             form[key + '_lr_x'], form[key + '_lr_y']])
        return coordinates

    @requires_auth
    def get(self, img_id=None):
        username = request.authorization.username
        obj = self.get_object(username, img_id)
        if obj is None:
            return render_template(self.template)

        filename = obj['filename']
        img_id = obj['id']
        img_size = map(int, obj['size'].split(','))
        if obj['labeled']:
            coordinates = {col[0]: map(int, obj[col[0]].split(',')) for col in VARIABLE_COLUMNS}
        else:
            coordinates = {col[0]: None for col in VARIABLE_COLUMNS}
        prev, next_ = self.get_prev_and_next(img_id)
        return render_template(self.template, filename=filename,
                               img_size=img_size,
                               coordinates=coordinates,
                               coordinates_json=json.dumps(coordinates),
                               prev=prev, next=next_,
                               n_of_landmark_features=NUMBER_OF_LANDMARK_FEATURES)

    @requires_auth
    def post(self, img_id=None):
        filename = request.form['filename']
        coordinates = self.get_coordinates(request.form)
        self.save_coordinates(coordinates, filename)
        return self.get()


class AdminView(View):
    @requires_auth
    def dispatch_request(self):
        if request.authorization.username != 'admin':
            return redirect(url_for('label_image'))
        cur = g.db.execute('select * from images')
        q_result = cur.fetchall()
        items = []
        for row in q_result:
            row_dict = {key: row[key] for key in row.keys()}
            items.append(row_dict)
        return render_template('admin.html', items=items)


# Routing
#-----------------------------------------
label_image = LabelImageView.as_view('label_image')
admin_view = AdminView.as_view('admin')

app.add_url_rule('/image',
                 view_func=label_image)
app.add_url_rule('/image/<img_id>',
                 view_func=label_image)
app.add_url_rule('/admin',
                 view_func=admin_view)


if __name__ == "__main__":
    app.run()
