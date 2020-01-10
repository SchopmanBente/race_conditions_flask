import os
import os.path
import logging
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from flask import Flask
import logging
from flask_bootstrap import Bootstrap

class FakeDatabase:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.info("Thread %s: finishing update", name)


class RaceConditionExampleOne(object):
    """his is a example where a race condition occurs with 2 threads."""

    def __init__(self):
       self.database = FakeDatabase()

    def run_example(self):
        filename = 'example_one.log'
        logger = logging.getLogger()
        logging.basicConfig(filename=filename, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        f_handler = logging.FileHandler(filename)
        f_handler.setLevel(logging.INFO)
        logger.addHandler(f_handler)
        database = self.database

        logging.debug('This is a debug message')
        logging.info('This is an info message')
        logging.warning('This is a warning message')
        logging.error('This is an error message')
        logging.critical('This is a critical message')
        logging.error("Testing update. Starting value is %d.", self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for index in range(2):
                executor.submit(database.update, index)
                logger.error("value:",  index)
        logger.error("Testing update. Ending value is %d.", self.database.value)


class RaceConditionExampleTwo(object):
    """This is a example where a race condition occurs with 3 threads"""

    def __init__(self):
        self.database = FakeDatabase()


    def run_example(self):
        filename = 'example_two.log'
        logger = logging.getLogger()
        logging.basicConfig(filename=filename, level=logging.INFO)
        database = self.database
        logging.info("Testing update. Starting value is %d.", self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for index in range(2):
                executor.submit(self.database.update, index)
        logging.info("Testing update. Ending value is %d.", self.database.value)



class FakeDatabaseTwo:
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.error("Thread %s: starting update", name)
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logging.error("Thread %s: finishing update", name)


class RaceConditionExampleThree(object):
    """This a example where are is a lock"""

    def __init__(self):
        self.database  = FakeDatabaseTwo()

    def run_example(self):
        filename = 'example_three.log'
        logger = logging.getLogger()
        logging.basicConfig(filename=filename, level=logging.INFO)
        database = self.database
        logging.info("Testing update. Starting value is %d.", self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            for index in range(2):
                executor.submit(self.database.update, index)
        logging.info("Testing update. Ending value is %d.", self.database.value)

class DirFolderName(object):
    """docstring for."""

    def __init__(self,name):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        uploads = str((os.path,ROOT_DIR,os.path.dirname(os.path.realpath(__file__)) ,'app/static/logs/'))
        self.uploads_path = uploads

    def get_uploads_path(self):
        return self.uploads_path
