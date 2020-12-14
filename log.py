import logging


def logger_setup(caller_filename):
  """
  The following code sets up the logger.

  First, we create a specific logger that logs information from "__name__". Next, we
  set the level of the logger so that it logs all INFO log messages. We then create a
  file handler that receives the log messages and add it to our logger. Lastly, we
  format the log messages and apply the formatting to the file handler.
  """
  logger = logging.getLogger(caller_filename)  # create logger
  logger.setLevel(logging.INFO) # set logging level

  file_handler = logging.FileHandler('covid.log') # creat file handler
  logger.addHandler(file_handler) # add the file handler to the logger

  formatter = logging.Formatter('%(asctime)s : %(name)s : %(message)s')
  file_handler.setFormatter(formatter)  # apply logging format to file handler

  return logger


