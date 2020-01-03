import os,sys,datetime
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from IdeconOCRData.GenericResponseFolder.GenericResponse import GenericResponse


currentFileName=str(datetime.datetime.today().strftime(r"%Y-%m-%d"))#.strftime(r"%d-%m-%Y")

UPLOAD_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\IdeconOCRInvoiceImages\\"+currentFileName

try:
    if os.path.isfile(UPLOAD_FOLDER) is False:
        os.mkdir(UPLOAD_FOLDER)
except FileExistsError:
    pass

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           get_extension(filename) in ALLOWED_EXTENSIONS

def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def upload_file(file):
    if allowed_file(file.filename):
        file_count=len([f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))])
        filename = secure_filename("InvoiceImage-"+currentFileName)
        # +"-"+datetime.datetime.today().strftime(r"%Y-%m-%d-%H-%M-%S")+"-"+str(file_count+1)+"."+get_extension(file.filename))
        imagePath=os.path.join(UPLOAD_FOLDER, filename)
        file.save(imagePath)
        return imagePath
    else:
        return None
        