import datetime
import json
from IdeconOCRGeneric import repository
import IdeconOCRHelper.SecurityFolder.SecurityOps as security
from flask import jsonify
from IdeconOCRData.GenericResponseFolder.GenericResponse import GenericResponse
from flask_restful import Resource
from IdeconOCRData.POCOs.User import User
import jwt
import IdeconOCRData.RequestModels.UserOpsModels.LoginRequestModel as lgnModel
import IdeconOCRData.RequestModels.UserOpsModels.RegisterRequestModel as regModel 
from IdeconOCRData.InAppModels.InAppUserModel import InAppUserModel as InAppModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

class Login(Resource):
    def post(self):        
        reqData=lgnModel.parser.parse_args()
        try:
            print("Deneme")
            loggedUser=User.query.filter(User.Username == reqData["username"]).first()
            print(loggedUser.to_dict())
            if loggedUser:
                realPassword=loggedUser.Password
                if security.verify_hash(reqData["password"],realPassword):
                    access_token = create_access_token(loggedUser.Username,False,datetime.timedelta(hours=12),loggedUser.to_dict())                  
                    response=GenericResponse("200","success",access_token)
                    return jsonify(response.__dict__)
                else:
                    response = GenericResponse("401","Password is incorrect!")
                    return jsonify(response.__dict__)
            else:
                response = GenericResponse("401","Username is incorrect!")
                return jsonify(response.__dict__)
                
        except Exception as e:
            response = GenericResponse("400","An error occured! Error: "+str(e))
            return jsonify(response.__dict__)

class GetUsers(Resource):
    @jwt_required
    def get(self):
        Users=repository.Query("SELECT * FROM UserTable")

        return jsonify(Users.__dict__)

class CreateUser(Resource):
    def post(self):
        reqData=regModel.parser.parse_args()

        try:
            username=reqData["username"]
            name=reqData["name"]
            surname=reqData["surname"]
            password=security.generate_hash(reqData["password"])
            
            userCreateSQL="INSERT INTO UserTable(Name,Surname,Username,Password) VALUES('{}','{}','{}','{}')".format(name,surname,username,password)

            repository.Execute(userCreateSQL)

            response=GenericResponse("200","User created successfully!")
            return jsonify(response.__dict__)
            

        except Exception as e:
            response = GenericResponse("400","An error occured! Error: "+str(e))
            return jsonify(response.__dict__)