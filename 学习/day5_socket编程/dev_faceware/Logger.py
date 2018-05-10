#coding: utf-8
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

#fileHandler = logging.FileHandler("log.txt")
#fileHandler.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s][%(filename)s][line:%(lineno)d][%(levelname)s] ## %(message)s")
consoleHandler.setFormatter(formatter)

#logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

