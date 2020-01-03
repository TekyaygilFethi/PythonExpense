from flask_restful import Api
import IdeconOCRGeneric.GenericFlask as gflask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,redirect
import IdeconOCRBusiness.RepositoryFolder.Repository as repo
from flask_jwt_extended import JWTManager

app=gflask.getFlask(__name__)

repository=repo.Repository(app)

jwt = JWTManager(app)
api=Api(app)
db=SQLAlchemy(app)