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

    try:
        filename = "example_one.log"
        path = '/home/bente/Documents/inholland/1920-4.2-security/workshops-securify/flask_race_conditions/app/static/logs/example_one.log'
        return send_from_directory(path, filename, as_attachment=False)
    except FileNotFoundError as fnf_error:
        print(fnf_error)

@app.route('/example_two')
def example_two():
    log = RaceConditionExampleTwo()
    csv = log.run_example();
    try:
        filename = "example_two.log"
        path = '/home/bente/Documents/inholland/1920-4.2-security/workshops-securify/flask_race_conditions/app/static/logs/example_two.log'
        #return send_file(path,attachment_filename=filename)
        return send_from_directory(path,filename,as_attachment=False)
       # return send_file(path, attachment_filename=filename)
    except FileNotFoundError as fnf_error:
        print(fnf_error)


@app.route('/hi')
def hello_world():
    log = RaceConditionExampleTwo()
    csv = log.run_example();
    try:
        filename = "raw_data.txt"
        path = 'app/static/logs/raw_data.txt'
        #return send_file(path,attachment_filename=filename)
        return send_from_directory(path, filename, as_attachment=True)
    # return send_file(path, attachment_filename=filename)
    except FileNotFoundError as fnf_error:
        print(fnf_error)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404