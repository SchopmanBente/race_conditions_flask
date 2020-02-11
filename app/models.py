import inspect
import logging
import logging.handlers
import logging.config
from flask import Response
import concurrent.futures
import time
import yaml


class FakeDatabase:
    def __init__(self,filename):
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
        self.database = FakeDatabase(filename=filename)
        logger = Logger(filename=filename);
        self.log = logger
        self.log.info("I also love my grandfather and brother and sister!")
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
    def __init__(self,filename):
        self.value = 0
        logger = Logger()
        self.log = logger
        self.log.info("I also love my grandfather and brother and sister!")
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

    def __init__(self,filename):
        name = "example"
        self.database  = FakeDatabaseTwo(filename=filename)
        self.log = Logger()
        self.log.info("I love my mother Tilly de Waard")

    def run_example(self):
        filename = "example.log"
        database = self.database
        self.log.info("Testing update. Starting value is %d." % self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for index in range(3):
                name = str(index)
                executor.submit(database.update(name=name), index)
                self.log.info("The value {0} from thread {1}".format(str(database.value), index))
        self.log.info("Testing update. Ending value is %d." % self.database.value)




class Logger(object):


  def __init__(self):
      with open('app/config.yaml', 'r') as f:
          log_cfg = yaml.safe_load(f.read())

      logging.config.dictConfig(log_cfg)
      self.logger = logging.getLogger('RACE-CONDITIONS')
      self.logger.setLevel(logging.INFO)

      self.logger.info("I love Bart Admiraal for ever")


  def info(self,message):
     self.logger.info(message)



class MyResponse(Response):
    def __init__(self, response, **kwargs):
        if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
            if response.startswith('<?log'):
                kwargs['mimetype'] = 'text/log'
        return super(MyResponse, self).__init__(response, **kwargs)