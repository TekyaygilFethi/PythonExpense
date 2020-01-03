from flask import jsonify
from IdeconOCRData.GenericResponseFolder.GenericResponse import GenericResponse
from IdeconOCRGeneric import repository
from flask_restful import Resource
import IdeconOCRData.RequestModels.CategoryOpsModels.CreateCategoryRequestModel as catReqModel



class CreateCategory(Resource):
    def post(self):
        reqData=catReqModel.parser.parse_args()

        try:
            catName=reqData["categoryName"]

            catCreateQuery="INSERT INTO CategoryTable(CategoryName) VALUES('{}')".format(catName)

            repository.Execute(catCreateQuery)
            response=GenericResponse("200","Category created succesfully!")
            return jsonify(response.__dict__)
        except Exception as e:
            response=GenericResponse("400","An error occured! Error: "+str(e))
            return jsonify(response.__dict__)
