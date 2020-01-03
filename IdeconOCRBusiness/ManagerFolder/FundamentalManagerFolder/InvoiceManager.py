#region Imports
import datetime,jwt
from flask import jsonify,request
from IdeconOCRData.GenericResponseFolder.GenericResponse import GenericResponse
from IdeconOCRGeneric import repository
from flask_restful import Resource
import IdeconOCRBusiness.DataConversionFolder.TupleConversion as tplConversion
import IdeconOCRData.RequestModels.InvoiceOpsModels.CreateInvoiceRequestModel as invReqModel
from IdeconOCRData.TrainOpsDataFolder.TrainOpsDataTag import TrainOpsDataTag
from IdeconOCRData.TrainOpsDataFolder.TrainOpsData import TrainOpsData
from IdeconOCRTrain.TrainDocFolder.TrainDocOps import AIDoc
import IdeconOCRHelper.UploadOpsFolder.Upload as uploadManager
import IdeconOCRVision.GoogleVision.VisionApi as api
import spacy
from spacy.pipeline import EntityRecognizer
import IdeconOCRVision.BaseRegexFolder.BaseRegex as baseRegex

import IdeconOCRVision.Regex.DateRegex as call
#endregion

class CreateInvoice(Resource):
    def post(self):
        reqData=invReqModel.parser.parse_args()

        try:
            #region Get Values from Request
            rawData=reqData["rawData"]
            invDateReqDataTag=reqData["date"] #trainopstag tipinde value prop unda
            invNoReqDataTag=reqData["invoiceNumber"] #trainopstag tipinde
            compNameReqDataTag=reqData["companyName"] #trainopstag tipinde
            vatTotalReqDataTag=reqData["vatTotal"] #trainopstag tipinde
            invTotalReqDataTag=reqData["invoiceTotal"] #trainopstag tipinde
            isTest=reqData["isTest"]
            #endregion

            #region Process TrainOpsDataTag props
            invDateDataTag=TrainOpsDataTag(invDateReqDataTag.startIndex,invDateReqDataTag.endIndex,invDateReqDataTag.tag,invDateReqDataTag.value)
            invNoDataTag=TrainOpsDataTag(invNoReqDataTag.startIndex,invNoReqDataTag.endIndex,invNoReqDataTag.tag,invNoReqDataTag.value)
            compNameDataTag=TrainOpsDataTag(compNameReqDataTag.startIndex,compNameReqDataTag.endIndex,compNameReqDataTag.tag,compNameReqDataTag.value)
            vatTotalDataTag=TrainOpsDataTag(vatTotalReqDataTag.startIndex,vatTotalReqDataTag.endIndex,vatTotalReqDataTag.tag,vatTotalReqDataTag.value)
            invTotalDataTag=TrainOpsDataTag(invTotalReqDataTag.startIndex,invTotalReqDataTag.endIndex,invTotalReqDataTag.tag,invTotalReqDataTag.value)
            #endregion

            #region Writing to txt file
            invDateTuple=tplConversion.DataTagToTuples(invDateReqDataTag)
            invNoTuple=tplConversion.DataTagToTuples(invNoReqDataTag)
            compNameTuple=tplConversion.DataTagToTuples(compNameReqDataTag)
            vatTotalTuple=tplConversion.DataTagToTuples(vatTotalReqDataTag)
            invTotalTuple=tplConversion.DataTagToTuples(invTotalReqDataTag)


            trainData=TrainOpsData(rawData,compNameTuple,invTotalTuple,invDateTuple,invNoTuple,vatTotalTuple)

            aiDoc=AIDoc()

            aiDoc.write_to_file(trainData)

            #endregion

            #region If not test write to db
            if isTest==False:
                #region Extract Values from DataTag object
                invTotal=invTotalDataTag.value
                vatTotal=vatTotalDataTag.value
                invDate=invDateDataTag.value
                invNo=invNoDataTag.value
                compName=compNameDataTag.value
                #endregion
                
                UploadDate=datetime.datetime.now()
                VATRate=invTotal/vatTotal
                userID=reqData["userID"]
                categoryID=reqData["categoryID"]
                invCreateQuery="INSERT INTO InvoiceTable(Date,UploadDate,InvoiceNumber,CompanyCode,VATRate,VATTotal,InvoiceTotal,userID,categoryID) VALUES ('{}','{}','{}','{}','{}','{}','{}',{},{})".format(invDate,UploadDate,invNo,compName,VATRate,vatTotal,invTotal,userID,categoryID)
                repository.Execute(invCreateQuery)
            #endregion

            response=GenericResponse("200","Invoice created successfully! Test Mode: "+str(isTest))
            return jsonify(response.__dict__)
        except Exception as e:
            response=GenericResponse("400","An error occured! Error: "+str(e))
            return jsonify(response.__dict__)

class UploadInvoice(Resource):
    # @jwt_required
    def post(self):
         #region Upload Call
        
        for i in request.files:
            print(i)

        if 'file' not in request.files:
            return jsonify(GenericResponse("400","No file part").__dict__)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return jsonify(GenericResponse("400","No selected file").__dict__)
        if file:
            path = uploadManager.upload_file(file)
        
            texts = api.detect_text(path)

        text = ' '.join(texts)
        nlp = spacy.load("IdeconOCRTrainModelSets\\trainModel")

        doc = nlp(text)
        
        tupleList=[]
        for ent in doc.ents:
            tupleList.append((ent.start_char,ent.end_char,ent.label_,ent.text))
        return jsonify(GenericResponse("200","success",tupleList).__dict__)

        #endregion

class UploadTestInvoice(Resource):
    def post(self):
        textList=[]
        if 'file' not in request.files:
            return jsonify(GenericResponse("400","No file part").__dict__)
        # files = request.files['file']
        files = request.files.getlist("file")
        # if user does not select file, browser also
        # submit a empty part without filename
        if [file.filename for file in files if file.filename=='']:
            return jsonify(GenericResponse("400","No selected file").__dict__)
        if files:
            for file in files:
                print(file.filename)
                try:
                    path = uploadManager.upload_file(file)
                    texts = api.detect_text(path)
                    text = ' '.join(texts)
                    if 'multinet' in text.lower():
                        return jsonify(GenericResponse("400","Multinet fişi gönderemezsiniz!").__dict__)
                    else:
                        textList.append(text)
                        regexDict=baseRegex.findRegexes(text)
                        
                        nlp = spacy.load("IdeconOCRTrainModelSets\\trainModel")

                        doc = nlp(text)
        
                        tupleList=[]
                        for ent in doc.ents:
                            tupleList.append((ent.start_char,ent.end_char,ent.label_,ent.text,False))

                        for tupleObj in tupleList:
                            tag=tupleObj[2]
                            if tag!="COMPANY" and tag!="INVOICENO":
                                spacyValue=tupleObj[3]
                                regexValue=regexDict[tupleObj[2]]

                                if spacyValue!=regexValue or (spacyValue.replace("-","/"))!=regexValue or (spacyValue.replace(".","/"))!=regexValue:
                                    index=text.find(str(regexValue))
                                    if index !=-1:
                                        tupleList[tupleList.index(tupleObj)]=(index,index+len(str(regexDict[tupleObj[2]])),tupleObj[2],regexDict[tupleObj[2]],True)
                            #regex ile spacy farklı ise ve regexten gelen text'İn içinde yoksa spacy den geleni al

                        return jsonify(GenericResponse("200","success",tupleList).__dict__)



                        # return jsonify(GenericResponse("200","success",regexDict).__dict__)
                        # textList.append("tarih: {}".format(call.find_dates(text)))


                except Exception as e:
                    return jsonify(GenericResponse("400",str(e)).__dict__)

        return jsonify(GenericResponse("200","success",textList).__dict__)
        

    