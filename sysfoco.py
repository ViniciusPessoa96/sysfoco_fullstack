from flask import Flask

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from views_api import *
from views_pages import *

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port='5002', debug=True)