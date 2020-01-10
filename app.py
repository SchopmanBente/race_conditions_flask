from flask import Flask, make_response, send_file, Response
from flask_bootstrap import Bootstrap
from app.models import MyResponse


app = Flask(__name__, template_folder='../templates')
app.response_class = MyResponse

app.debug = True


bootstrap = Bootstrap(app)
