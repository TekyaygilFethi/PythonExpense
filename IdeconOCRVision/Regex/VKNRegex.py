import re
import datetime
import pandas as pd
import Levenshtein
from date_detector import Parser
import IdeconOCRHelper.ValidationFolder.NumberValidation as numberValidation
import IdeconOCRHelper.VerificationFolder.VKNVerification as vknVerification
import IdeconOCRHelper.VerificationFolder.TCNoVerification as tcVerification

parser = Parser()

spaceRegex=r"(?<=\d) (?=\d{3,4})"

regex =r"[0-9]{10,11}"

def get(text):
    val = None
    #text = text.replace(" ", "")
    val = process(text,regex)

    return val

def eliminateSpaces(text):
    matches=re.finditer(spaceRegex,text,re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        text.replace(match.group(0),"")
        return text

def process(text,regex):
    #first, find corresponding spaces and eliminate them
    newText=eliminateSpaces(text)
    matches = re.finditer(regex,newText, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        vkn = match.group(0)
        vkn=numberValidation.onlyNumberValidate(vkn)

        if len(vkn)==10:
            if vknVerification.vkn_verification(vkn):
        #seçilen tarihin içinde sadece rakam mı var yoksa yazıda varmı onu öğrenip tahmin yapıp geri gönderiyor
                return vkn
            else:
                return None
        elif len(vkn)==11:
            if tcVerification.tc_verification(vkn):
                return vkn
            else:
                return None
                