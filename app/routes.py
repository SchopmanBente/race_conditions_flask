from app import app
from flask import render_template, make_response, send_from_directory
from flask_bootstrap import Bootstrap

from .models import  RaceConditionExampleOne, RaceConditionExampleTwo, RaceConditionExampleThree
from os.path import dirname, realpath, join
import os
from os import path
from pathlib import Path

# this is a comment to get GitHub working again
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/race_conditions_example_one')
def example_two():
    log = RaceConditionExampleOne()
    logger = log.run_example();
    try:
       filename = "example_one.log"
       uploads_class = DirFolderName(filename)
       uploads = uploads_class.get_uploads_path
       return Response(
            filename,
            mimetype="text/log",
            headers={"Content-disposition":
                     "attachment; filename=example_one.log"})
    except FileNotFoundError as fnf_error:
       print(fnf_error)

# @app.route('/race_conditions_example_two')
#def example_two():
#    log = RaceConditionExampleTwo()
#    logger = log.run_example();
#    try:
#       filename = "example_two.log"
       #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
       #uploads = os.path.join(ROOT_DIR, dirname(realpath(__file__)) + '/static/logs/')
       #return send_from_directory(directory=uploads, filename=filename)
#    except FileNotFoundError as fnf_error:
#       print(fnf_error)


@app.route('/race_conditions_example_three')
def example_three():
    log = RaceConditionExampleThree()
    logger = log.run_example();
    try:
       filename = "example_three.log"
       #ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
      # uploads = os.path.join(ROOT_DIR, dirname(realpath(__file__)) + '/static/logs/')
       #return send_from_directory(directory=uploads, filename=filename)
    except FileNotFoundError as fnf_error:
       print(fnf_error)
