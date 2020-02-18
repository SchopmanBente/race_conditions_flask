import inspect
import logging
import logging.handlers
import logging.config
from flask import Response
import concurrent
import time
import yaml


class FakeDatabase:
    def __init__(self):
        self.value = 0
        self.log = Logger()
        self.log.info("Working with FakeDatabase")

    def update(self, name):
        self.log.info("Working with FakeDatabase")
        self.log.info("FakeDatabase is giving info right now")
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
        self.database = FakeDatabase()
        logger = Logger()
        self.log = logger

    def run_example(self):
        name = "example.log"

        database = self.database
        self.log.info("Working with FakeDatabase")
        self.log.info("Testing update. Starting value is %d." % self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for index in range(2):
                name =  str(index)
                executor.submit(database.update(name=name), index)
                self.log.info("The value {0} from thread {1}".format(database.value, index))

        self.log.info("Testing update. Ending value is %d." % self.database.value)




class FakeDatabaseTwo:
    def __init__(self):
        self.value = 0
        logger = Logger()
        self.log = logger
        self.log.info("Working with FakeDatabaseTwo")

    def update(self, name):
        self.log.info("FakeDatabaseTWo is giving info right now")
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
        self.database  = FakeDatabaseTwo()
        self.log = Logger()
        self.log.info("Working with FakeDatabaseTwo")

    def run_example(self):
        self.log.info("Working with FakeDatabaseTwo")
        database = self.database
        self.log.info("Testing update. Starting value is %d." % self.database.value)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for index in range(3):
                name = str(index)
                executor.submit(database.update(name=name), index)
                self.log.info("The value {0} from thread {1}".format(database.value, index))
        self.log.info("Testing update. Ending value is %d." % self.database.value)




class Logger(object):


  def __init__(self):
      self.logger = logging.basicConfig(filename='example.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
      self.logger = logging.getLogger('RACE-CONDITIONS')
      self.logger.setLevel(logging.INFO)




  def info(self,message):
      self.logger.info(message)



class MyResponse(Response):
    def __init__(self, response, **kwargs):
        if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
            if response.startswith('<?log'):
                kwargs['mimetype'] = 'text/log'
        return super(MyResponse, self).__init__(response, **kwargs)