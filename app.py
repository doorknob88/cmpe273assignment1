import json
import os
import uuid

import redis
import simplejson as json
from flask import Flask, request, redirect
from flask_json import FlaskJSON
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = set(['py'])

app = Flask(__name__)
r = redis.Redis(unix_socket_path='/tmp/redis.sock')
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
FlaskJSON(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
key = uuid.uuid4().hex


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/v1/scripts', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'data' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['data']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))

            name = file.filename[0:3]
            r.set(key, name.encode('utf-8'))
            data = {'script-id': key}
            return "201 Created " + json.dumps(data)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/api/v1/scripts/<script_id>', methods=['GET'])
def get_file(script_id):
    key = script_id
    check = r.get(key).decode('utf-8') + ".py"
    return "200 OK \n", exec(open("temp/" + check).read())


if (__name__ == "__main__"):
    app.run(port=8000)
