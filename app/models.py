import inspect
import logging
import logging.handlers
from flask import Response
import concurrent
import time
import os


class FakeDatabase:
    def __init__(self,filename, function):
        self.value = 0
        self.logfile = filename
        logger_new = Logger(console_level=logging.INFO, file_level=logging.INFO, log_file=filename,
                            function_name=function);
        self.log = logger_new.function_logger()

    def update(self, name):
        self.log.error("Thread {0}: starting update".format(name))
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        self.log.info("Thread {0} has this value {1}".format(name, self.value))
        self.log.error("Thread {0}: finishing update".format(name))


class RaceConditionExampleOne(object):
    """his is a example where a race condition occurs with 2 threads."""

    def __init__(self):
        filename = "example_one.log"
        self.database = FakeDatabase(filename=filename,function="example_one")

    def run_example(self):
        name = "example_one"
        logger_new = Logger(console_level=logging.INFO, log_file=name + '.log', function_name=name,
                            file_level=logging.INFO);
        log = logger_new.function_logger()
        database = self.database

        log.error("Testing update. Starting value is %d." % self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for index in range(2):
                name =  str(index)
                executor.submit(database.update(name=name), index)
        log.error("Testing update. Ending value is %d." % self.database.value)




class FakeDatabaseTwo:
    def __init__(self, function_name, filename=None):
        self.value = 0
        logger_new = Logger(console_level=logging.INFO,file_level=logging.INFO,log_file=filename,function_name=function_name);
        self.log = logger_new.function_logger()

    def update(self, name):

        self.log.error("Thread {0}: starting update".format(name))
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        self.log.info("Thread {0} has this value {1}".format(name,self.value))
        self.log.error("Thread {0}: finishing update".format(name))


class RaceConditionExampleTwo(object):
    """This a example where are is a lock"""

    def __init__(self):
        name = "example_three"
        self.database  = FakeDatabaseTwo(function_name=name, filename=name +".log")

    def run_example(self):
        filename = "example_three.log"
        logger_new = Logger(log_file=filename,function_name="example_three",console_level=logging.INFO,file_level=logging.INFO);
        log = logger_new.function_logger()
        database = self.database
        log.info("Testing update. Starting value is {0}.".format(database.value))
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for index in range(3):
                name = str(index)
                executor.submit(database.update(name=name), index)
                log.info("The value {0} from thread {1}".format(database.value,index))
        log.info("Testing update. Ending value is {0}.".format(database.value))




class Logger(object):

    def __init__(self, function_name,console_level, file_level, log_file):
        self.log_file = log_file;
        self.function_name = function_name;
        self.console_level = console_level;
        self.file_level = file_level

    def function_logger(self):

        logging.basicConfig(filename=self.log_file, level=logging.DEBUG)
        return  logging

class MyResponse(Response):
    def __init__(self, response, **kwargs):
        if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
            if response.startswith('<?log'):
                kwargs['mimetype'] = 'text/log'
        return super(MyResponse, self).__init__(response, **kwargs)