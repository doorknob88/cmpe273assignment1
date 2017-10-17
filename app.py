from _curses import flash

import os, json

import numpy as np
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
data = dict()
counter = 0


@app.route("/api/v1/scripts", methods=['POST'])
def uploader():
    return "Upload path"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            global counter
            data[counter] = file.filename
            np.save('data.npy', data)
            counter += 1
            execfile('upload/foo.py')
            return "File received: script_id value: "+str(counter-1)+" <br> go to localhost:8000/api/v1/scripts/"+str(counter-1)+" to see your file executed."
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


from flask import send_from_directory


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/api/v1/scripts/<int:script_id>', methods=['GET', 'POST'])
def run(script_id):
    global data
    data = np.load('data.npy').item()
    if data[script_id] != '':
        execfile('upload/'+data[script_id])
    return 'script_id: '+str(script_id)+' Result: '+str(execfile('upload/'+data[script_id]))


if __name__ == '__main__':
    app.run(port=8000)
