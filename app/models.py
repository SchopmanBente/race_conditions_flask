import inspect
import logging
import logging.handlers
import logging.config
from flask import Response
import concurrent
import time
import yaml


class FakeDatabase:
    def __init__(self,filename, function):
        self.value = 0
        self.logfile = filename
        self.log = Logger()

    def update(self, name):
        self.log.info("Thread {0}: starting update".format(name))
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        self.log.info("Thread {0} has this value {1}".format(name, self.value))
        self.log.info("Thread {0}: finishing update".format(name))


class RaceConditionExampleOne(object):
    """his is a example where a race condition occurs with 2 threads."""

    def __init__(self):
        filename = "example.log"
        self.database = FakeDatabase(filename=filename,function="example_one")
        logger = Logger();
        self.log = logger
    def run_example(self):
        name = "example.log"

        database = self.database

        self.log.info("Testing update. Starting value is %d." % self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for index in range(2):
                name =  str(index)
                executor.submit(database.update(name=name), index)
                self.log.info("The value {0} from thread {1}".format(database.value, index))

        self.log.info("Testing update. Ending value is %d." % self.database.value)




class FakeDatabaseTwo:
    def __init__(self, function_name, filename=None):
        self.value = 0
        logger = Logger();
        self.log = logger

    def update(self, name):

        self.log.info("Thread {0}: starting update".format(name))
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        self.log.info("Thread {0} has this value {1}".format(name,self.value))
        self.log.info("Thread {0}: finishing update".format(name))


class RaceConditionExampleTwo(object):
    """This a example where are is a lock"""

    def __init__(self):
        name = "example"
        self.database  = FakeDatabaseTwo(function_name=name, filename=name +".log")
        self.logger = Logger();

    def run_example(self):
        filename = "example.log"
        database = self.database
        self.logger.info("Testing update. The starting value is %d.".format(database.value))
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for index in range(3):
                name = str(index)
                executor.submit(database.update(name=name), index)
                self.logger.info("The value %d from thread %d",format(database.value,index))
        self.logger.info("Testing update. The ending value is %d.".format(database.value))




class Logger(object):


  def __init__(self):
      with open('app/config.yaml', 'r') as f:
          config = yaml.safe_load(f.read())
          logging.config.dictConfig(config)

      logger = logging.getLogger('logger')
      logger.info("Is working for you now")
      self.logger = logger

  def info(self,message):
     self.logger.info(message)

class LogSwitcher(object):
    def __init__(self,logger,level):
        self.logger = logger
        self.log_level = level

    def log(log_level,message):
        return {
            logging.INFO: self.logger.info(message)
        }.get(log_level, self.logger.debug(message))

class MyResponse(Response):
    def __init__(self, response, **kwargs):
        if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
            if response.startswith('<?log'):
                kwargs['mimetype'] = 'text/log'
        return super(MyResponse, self).__init__(response, **kwargs)