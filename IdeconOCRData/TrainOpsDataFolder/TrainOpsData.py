import sys
import os
sys.path.append(os.path.dirname(__file__))
import json

# from TrainOpsDataTag import TrainOpsDataTag

class TrainOpsData():
    def __init__(self,TEXT=None,COMPANY=None,AMOUNT=None,DATE=None,NO=None,KDV=None,trainData=None):
        self.TEXT=TEXT
        entityDict={}
        entityDict["entities"]=[AMOUNT,COMPANY,NO,DATE,KDV]
        if trainData is None:
            self.trainData=(TEXT,entityDict)
        else:
            self.trainData=trainData
        
    def __str__(self):
        return str(self.trainData)
   
    
        
  