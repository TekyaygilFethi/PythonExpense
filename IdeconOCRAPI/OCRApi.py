import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#region Imports
from IdeconOCRData.POCOs.Invoice import Invoice
from IdeconOCRData.POCOs.Category import Category
from IdeconOCRGeneric import api,app
import IdeconOCRDatabase.TableCreationFactories.TableCreationFactory as db_factory
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,redirect
#from IdeconOCRData.POCOs.User import User
import IdeconOCRData.POCOs.User as User
from IdeconOCRBusiness.AuthorizationWrapperFolder.AuthorizationWrapper import auth
import jwt
import IdeconOCRBusiness.ManagerFolder.FundamentalManagerFolder.UserManager as uManager
import IdeconOCRBusiness.ManagerFolder.FundamentalManagerFolder.CategoryManager as catManager
import IdeconOCRBusiness.ManagerFolder.FundamentalManagerFolder.InvoiceManager as invManager
from flask_jwt_extended import JWTManager
#endregion

db_factory.Create()

#User.initDB(db)

api.add_resource(uManager.Login,'/Login')
api.add_resource(uManager.GetUsers,'/GetUsers')
api.add_resource(uManager.CreateUser,'/CreateUser')
api.add_resource(invManager.CreateInvoice,'/CreateInvoice')
api.add_resource(invManager.UploadInvoice,'/UploadInvoice')
api.add_resource(invManager.UploadTestInvoice,'/UploadTestInvoice')
api.add_resource(catManager.CreateCategory,'/CreateCategory')


"""
@app.route('/getParaBirimleri',methods=['GET'])
@auth
def getParaBirimleri():
   decoded = jwt.decode("", app.config['SECRET_KEY'])
   return jsonify(2)
"""



if __name__ == "__main__":
   # app.run(debug=True)
   app.run()