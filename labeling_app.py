import sqlite3
from contextlib import closing
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response
from flask.views import MethodView, View

# Configuration etc.
#-----------------------------------------
app = Flask(__name__)
app.config.update(dict(
    DATABASE='/tmp/labeling_app.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

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
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

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
class LabelItemView(MethodView):

    def get_filename(self, img_id=None):
        if img_id is None:
            qstring = 'select filename from images where {0} is null limit 1'.format(self.variable)
        else:
            qstring = 'select filename from images where id = {0}'.format(img_id)
        cur = g.db.execute(qstring)
        q_result = cur.fetchall()
        return q_result[0][0] if len(q_result) else None

    def save_coordinates(self, coordinates, filename):
        qstring = 'update images set {0}=? where filename=?'.format(self.variable)
        g.db.execute(qstring, (','.join(coordinates), filename,))
        g.db.commit()

    def get_coordinates(self, form):
        raise NotImplementedError()

    @requires_auth
    def get(self, img_id=None):
        filename = self.get_filename(img_id)
        return render_template(self.template, filename=filename)

    @requires_auth
    def post(self, img_id=None):
        filename = request.form['filename']
        coordinates = self.get_coordinates(request.form)
        self.save_coordinates(coordinates, filename)
        return self.get()


class LabelFaceView(LabelItemView):
    variable = 'face_coordinates'
    template = 'label_face.html'
    def get_coordinates(self, form):
        return [request.form['ul_x'], request.form['ul_y'],
                request.form['lr_x'], request.form['lr_y']]


class LabelEyesView(LabelItemView):
    variable = 'eye_coordinates'
    template = 'label_eyes.html'
    def get_coordinates(self, form):
        leye_coordinates = [request.form['l_ul_x'], request.form['l_ul_y'],
                            request.form['l_lr_x'], request.form['l_lr_y']]
        reye_coordinates = [request.form['r_ul_x'], request.form['r_ul_y'],
                            request.form['r_lr_x'], request.form['r_lr_y']]
        return leye_coordinates + reye_coordinates


class LabelMouthView(LabelItemView):
    variable = 'mouth_coordinates'
    template = 'label_face.html'
    def get_coordinates(self, form):
        return [request.form['ul_x'], request.form['ul_y'],
                request.form['lr_x'], request.form['lr_y']]


class LabelNoseView(LabelItemView):
    variable = 'nose_coordinates'
    template = 'label_face.html'
    def get_coordinates(self, form):
        return [request.form['ul_x'], request.form['ul_y'],
                request.form['lr_x'], request.form['lr_y']]


class ListImagesView(View):
    @requires_auth
    def dispatch_request(self):
        cur = g.db.execute('select * from images')
        q_result = cur.fetchall()
        items = [{'id': x[0], 'filename': x[1],
                   'face_coordinates': x[2],
                   'eye_coordinates': x[3],
                   'mouth_coordinates': x[4],
                   'nose_coordinates': x[5]} for x in q_result]
        return render_template('list.html', items=items)


# Routing
#-----------------------------------------
face_view = LabelFaceView.as_view('label_face')
eyes_view = LabelEyesView.as_view('label_eyes')
mouth_view = LabelMouthView.as_view('label_mouth')
nose_view = LabelNoseView.as_view('label_nose')
list_view = ListImagesView.as_view('list_images')

app.add_url_rule('/face',
                 view_func=face_view)
app.add_url_rule('/face/<img_id>',
                 view_func=face_view)
app.add_url_rule('/eyes',
                 view_func=eyes_view)
app.add_url_rule('/eyes/<img_id>',
                 view_func=eyes_view)
app.add_url_rule('/mouth',
                 view_func=mouth_view)
app.add_url_rule('/mouth/<img_id>',
                 view_func=mouth_view)
app.add_url_rule('/nose',
                 view_func=nose_view)
app.add_url_rule('/nose/<img_id>',
                 view_func=nose_view)
app.add_url_rule('/list',
                 view_func=list_view)


if __name__ == "__main__":
    app.debug = True
    app.run()
