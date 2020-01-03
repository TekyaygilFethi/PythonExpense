from flask_mysqldb import MySQL
from IdeconOCRGeneric import GenericFlask as gflask

class IdeconDbContext():
    def __init__(self, app):
        self.app=app

    def getContext(self):
        with self.app.app_context():
            mysql=MySQL(self.app)
            return mysql
