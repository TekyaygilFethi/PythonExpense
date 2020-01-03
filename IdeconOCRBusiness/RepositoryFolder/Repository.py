from flask_mysqldb import MySQL
import IdeconOCRDatabase.IdeconOCRDbContext as db

class Repository():
    def __init__(self,app):
        ideconDb=db.IdeconDbContext(app)
        self.DbContext=ideconDb.getContext()
    
    def Query(self,qry,parameters=None,type="all"):
        localCursor=self.DbContext.connection.cursor()
        if parameters==None:
            localCursor.execute(qry)
        else:
            localCursor.execute(qry,tuple(parameters))

        if type=="all":
            return localCursor.fetchall()
        else:
            return localCursor.fetchone()
    
    def Execute(self,qry,parameters=None):
        try:
            localCursor=self.DbContext.connection.cursor()
            if parameters==None:
                localCursor.execute(qry)
            else:
                localCursor.execute(qry,tuple(parameters))

            self.DbContext.connection.commit()
            localCursor.close()
        except Exception as e:
            raise Exception(str(e)+" Query:{}".format(qry))




