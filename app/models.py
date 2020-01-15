import os
import os.path
import logging
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, Response
from math import log
import logging
import time
import inspect
from time import sleep
from flask_bootstrap import Bootstrap

class FakeDatabase:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.info("Thread %s: starting update" % name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info("Thread %s: finishing update" % name)


class RaceConditionExampleOne(object):
    """his is a example where a race condition occurs with 2 threads."""

    def __init__(self):
       self.database = FakeDatabase()

    def run_example(self):
        filename = "example_one.log"
        logger_new = Logger();
        log = logger_new.function_logger(console_level=logging.ERROR, logfile=filename)
        database = self.database

        log.debug('This is a debug message')
        log.info('This is an info message')
        log.warning('This is a warning message')
        log.error('This is an error message')
        log.critical('This is a critical message')
        log.error("Testing update. Starting value is %d." % self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for index in range(2):
                name =  str(index)
                executor.submit(database.update(name=name), index)

        log.error("Testing update. Ending value is %d." % self.database.value)


class RaceConditionExampleTwo(object):
    """This is a example where a race condition occurs with 3 threads"""

    def __init__(self):
        self.database = FakeDatabase()


    def run_example(self):
        filename = "example_two.log"

        logger_new = Logger();
        log = logger_new.function_logger(console_level=logging.ERROR, logfile=filename)
        logging.basicConfig(filename=filename,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
        database = self.database
        log.info("Testing update. Starting value is %d."% database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for index in range(2):
                name = str(index)
                executor.submit(database.update(name=name), index)
        log.info("Testing update. Ending value is %d."% database.value)



class FakeDatabaseTwo:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.error("Thread %s: starting update" % name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.error("Thread %s: finishing update" % name)


class RaceConditionExampleThree(object):
    """This a example where are is a lock"""

    def __init__(self):
        self.database  = FakeDatabaseTwo()

    def run_example(self):
        filename = "example_three.log"
        logger_new = Logger();
        log = logger_new.function_logger(console_level=logging.ERROR, logfile=filename)
        logging.basicConfig(filename=filename,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
        database = self.database
        log.info("Testing update. Starting value is %d." % database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for index in range(3):
                name = str(index)
                executor.submit(database.update(name=name), index)
        log.info("Testing update. Ending value is %d." % database.value)

class DirFolderName(object):
    """docstring for."""

    def __init__(self,name):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        uploads = str((os.path,ROOT_DIR,os.path.dirname(os.path.realpath(__file__)) ,''))
        self.uploads_path = uploads

    def get_uploads_path(self):
        return self.uploads_path



class Logger(object):

    def function_logger(file_level=None, console_level=None,logfile="example_one.log"):
        function_name = inspect.stack()[1][3]
        logger = logging.getLogger(function_name)
        logger.setLevel(logging.DEBUG)  # By default, logs all messages

        if console_level != None:
            ch = logging.StreamHandler()  # StreamHandler logs to console
            ch.setLevel(console_level)
            ch_format = logging.Formatter('%(asctime)s - %(message)s')
            ch.setFormatter(ch_format)
            logger.addHandler(ch)

        fh = logging.FileHandler(logfile.format(function_name))
        fh.setLevel(logging.INFO)
        fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
        fh.setFormatter(fh_format)
        logger.addHandler(fh)

        return logger


class MyResponse(Response):
    pass