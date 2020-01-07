from flask import Flask, make_response, send_file
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__, template_folder='../templates')
app.debug = True
app.config["LOGS"] = "logs"
app.config['UPLOAD_FOLDER'] = dirname(realpath(__file__)) + 'static/logs'


from app import routes

bootstrap = Bootstrap(app)
