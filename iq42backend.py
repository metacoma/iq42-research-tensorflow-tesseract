#!/usr/bin/python3
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
#from requests_toolbelt.multipart import decoder
from multipart import tob
import multipart as mp

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '3super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadEZ', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        data = request.data
        #s = str(data).split("\r")[0][16:]
        s = data[2:42]
        print("s is ", s)

        p = mp.MultipartParser(BytesIO(tob(data)),s)
        newFile = open("/tmp/screenshot.png", "wb")
        #newFile.write(data)
        newFile.write((p.parts()[0].value.encode("latin-1")))
        #print("Data size: {}".format(len(request.data)))
        
    return "OK"

@app.route('/')
def hello_world():
    return 'Hello, World!'


