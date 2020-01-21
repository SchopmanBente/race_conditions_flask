import os
from flask import Flask, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename

from app import app
from .models import DirFolderName, RaceConditionExampleOne, RaceConditionExampleThree


# this is a comment to get GitHub working again
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/race_conditions_example_one')
def example_one():
    log = RaceConditionExampleOne()
    logger = log.run_example();

    try:
        file_name = "example_one.log"
        filename = secure_filename(file.file_name)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('/race_conditions_example_one'))
       # return send_from_directory(uploads, file_name, as_attachment=True)
    except FileNotFoundError as fnf_error:
       print(fnf_error)

@app.route('/race_conditions_example_two')
def example_two():

    log = RaceConditionExampleOne()
    logger = log.run_example();
    try:
       file_name = "example_two.log"

       filename = secure_filename(file.file_name)
       file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       return redirect(url_for('/race_conditions_example_one'))
    except FileNotFoundError as fnf_error:
       print(fnf_error)

@app.route('/race_conditions_example_three')
def example_three():
    log = RaceConditionExampleThree()
    logger = log.run_example();
    try:
       file_name = "example_three.log"
       return send_file('/home/bente/Documents/inholland/1920-4.2-security/workshops-securify/flask_race_conditions/app/static/logs/example_three.log', attachment_filename=file_name)
     #  filename = secure_filename(file.file_name)
       #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
 #      return redirect(url_for('/race_conditions_example_one'))
    except FileNotFoundError as fnf_error:
       print(fnf_error)


@app.route('/return-files/')
def return_files_tut():
    try:
        print("Ga es werken ofzo")
        return send_file('/home/bente/Documents/inholland/1920-4.2-security/workshops-securify/flask_race_conditions/app/static/images/gedragsveranderingsmodel.png',attachment_filename='gedragsveranderingsmodel.png')
    except FileNotFoundError as fnf_error:
        print(fnf_error)