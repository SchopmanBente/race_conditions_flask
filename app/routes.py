from app import app
from flask import render_template, make_response, send_file, Response
from flask_bootstrap import Bootstrap
import logging
from .models import  DirFolderName, RaceConditionExampleOne, RaceConditionExampleTwo, RaceConditionExampleThree, MyResponse
from os import path
from os.path import dirname, realpath, join

from pathlib import Path

# this is a comment to get GitHub working again
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/race_conditions_example_one')
def example_one():
    logging.warning("boe!")
    log = RaceConditionExampleOne()
    logger = log.run_example();

    try:
        filename = "example_one.log"
        uploads_class = DirFolderName(filename)
        uploads = uploads_class.get_uploads_path
        return Response(
            logger,
            mimetype="text/log",
            headers={"Content-disposition":
                         "attachment; filename=example_one.log"})
        #return send_file(uploads,as_attachment=True, attachment_filename=filename)
    except FileNotFoundError as fnf_error:
       print(fnf_error)

@app.route('/race_conditions_example_two')
def example_two():

    log = RaceConditionExampleOne()
    logger = log.run_example();
    try:
       filename = "example_two.log"
       uploads_class = DirFolderName(filename)
       uploads = uploads_class.get_uploads_path
       return Response(
           logger,
           mimetype="text/log",
           headers={"Content-disposition":
                        "attachment; filename=example_two.log"})
    except FileNotFoundError as fnf_error:
       print(fnf_error)

@app.route('/race_conditions_example_three')
def example_three():
    log = RaceConditionExampleThree()
    logger = log.run_example();
    try:
       filename = "example_three.log"
       uploads_class = DirFolderName(filename)
       uploads = uploads_class.get_uploads_path
       print(logger)
       return Response(
           logger,
           mimetype="text/log",
           headers={"Content-disposition":
                        "attachment; filename=example_three.log"})
    except FileNotFoundError as fnf_error:
       print(fnf_error)


@app.route("/getPlotCSV")
def getPlotCSV():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})
