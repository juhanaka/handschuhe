import sqlite3
from contextlib import closing
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response

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


@app.route('/', methods=['POST', 'GET'])
@requires_auth
def index():
    if request.method == 'POST':
        filename = request.form['filename']
        cur = g.db.execute('update images set labeled=1 where filename=?', (filename,))
        g.db.commit()
    cur = g.db.execute('select filename from images where labeled = 0 limit 1;')
    q_result = cur.fetchall()
    filename = q_result[0][0] if len(q_result) else None
    return render_template('display_image.html', filename=filename)


if __name__ == "__main__":
    app.debug = True
    app.run()
