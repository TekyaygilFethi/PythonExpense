from flask import Flask
import os,sys,datetime

def initFlask(name):
    app = Flask(name)
    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = r"****************"
    app.config["MYSQL_DB"] = "ideconocrdatabase"
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"
    app.config['SECRET_KEY'] = r'*************************'
    app.config["SQLALCHEMY_DATABASE_URI"]='mysql://root:Idecon1*@localhost/ideconocrdatabase'

    

    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



    return app

def getFlask(name):
    return initFlask(name)
