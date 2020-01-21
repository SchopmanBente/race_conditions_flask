from flask import Flask, make_response, send_file, Response
from flask_bootstrap import Bootstrap
from app.models import MyResponse


app = Flask(__name__, template_folder='../templates')
app.response_class = MyResponse

UPLOAD_FOLDER = 'flask_race_conditions/temp'

app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


bootstrap = Bootstrap(app)
