import re
import datetime
import pandas as pd
import Levenshtein
from date_detector import Parser
import functools

parser = Parser()

vatFinderRegex=r"%([0-9]{1,2})|% ([0-9]{1,2})" #group 2 den
vatRates=[1,1.01,1.08,1.18]
regex =r"[0-9]{1,}[\.\,][0-9]+[\.\,][0-9]{2}(\s|$)|[0-9]+[\.\,][0-9]{2}(\s|$)"

def get(text):
    val = None
    # text = text.replace(" ", "")
    val = process(text,regex)

    return val


def nth_repl(s, sub, repl, nth):
    find = s.find(sub)
    # if find is not p1 we have found at least one match for the substring
    i = find != -1
    # loop util we find the nth or we find no match
    while find != -1 and i != nth:
        # find + 1 means we start at the last match start index + 1
        find = s.find(sub, find + 1)
        i += 1
    # if i  is equal to nth we found nth matches so replace
    if i == nth:
        return s[:find]+repl+s[find + len(sub):]
    return s

def changeReagent(amount):

    if(amount.count('.') + amount.count(',') > 1):
        if(amount.find(".")<amount.find(",")):
            amount = (amount.replace(".","")).replace(",",".")
        elif(amount.count('.')==2):
            # amount = nth_repl(amount,".",",",2)
            amount = nth_repl(amount,".","",1)
        else:
            amount = amount.replace(",","")
    
    else:
        amount = amount.replace(",",".")

        

    return amount

def process(text,regex):
    #first, find corresponding spaces and eliminate them
    matches = re.finditer(regex,text, re.MULTILINE)
    totalVATRate=getAverageVATRates(text)
    
    amountList=[]
    maxAmount=0
    for matchNum, match in enumerate(matches, start=1):
        amount = float(changeReagent(match.group(0)))
        amountList.append(amount)

        if amount>maxAmount:
            maxAmount=amount
           
    vat=-1
    
    if totalVATRate != None:
        vat=maxAmount-(maxAmount/(1+totalVATRate))
    
    return {"KDV":vat,"AMOUNT":amount}

def getAverateVATRates(amountList):
    for amount in amountList:
        for vatRate in vatRates:
            amount-(amount/vatRate)


def getAverageVATRates(text):
    vats=[]
    matches = re.finditer(vatFinderRegex,text, re.MULTILINE)
    
    for matchNum, match in enumerate(matches, start=1):
        vat = match.group(1)
        vats.append(float(vat))
    
    if len(vats)==0:
        return None

    sumVAT=functools.reduce(lambda x,y : x+y,vats)
    return sumVAT/len(vats)

    
    