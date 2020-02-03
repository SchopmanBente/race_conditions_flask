from app import app
from flask import render_template, make_response, send_file, Response, send_from_directory
from flask_bootstrap import Bootstrap
import logging
from .models import   RaceConditionExampleOne, RaceConditionExampleTwo, MyResponse
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
    log = RaceConditionExampleOne()
    csv = log.run_example();
    print(csv)
    try:
        return Response(
            csv,
            mimetype="text/log",
            headers={"Content-disposition":
                         "attachment; filename=example.log"})
    except FileNotFoundError as fnf_error:
        print(fnf_error)

@app.route('/race_conditions_example_two')
def example_two():
    log = RaceConditionExampleTwo()
    csv = log.run_example();
    print(csv)
    try:
        return Response(
            csv,
            mimetype="text/log",
            headers={"Content-disposition":
                         "attachment; filename=example.log"})

    except FileNotFoundError as fnf_error:
        print(fnf_error)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


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