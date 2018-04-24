# -*- coding: utf-8 -*-
DB_TYPE = "mysql"
DRIVER = "pymysql"
HOST = "localhost"
DATABASE = "flask"
USERNAME = "root"
PORT = 3306
PASSWORD = "zql9988"
SQLALCHEMY_DATABASE_URI = "%s+%s://%s:%s@%s:%s/%s?charset=utf8" % (DB_TYPE, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False