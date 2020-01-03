import flask_sqlalchemy
from IdeconOCRGeneric import db
import datetime
from IdeconOCRData.POCOs.Category import Category
from IdeconOCRData.POCOs.User import User
from sqlalchemy_serializer import SerializerMixin

class Invoice(db.Model,SerializerMixin):
    __tablename__="InvoiceTable"

    # def __init__(self, Date,InvoiceNumber,CompanyCode,VATTotal,InvoiceTotal):
    #     self.Date=Date
    #     # self.UploadDate=datetime.datetime.now()
    #     self.InvoiceNumber=InvoiceNumber
    #     self.CompanyCode=CompanyCode
    #     self.VATTotal=VATTotal
    #     self.InvoiceTotal=InvoiceTotal
    #     self.VATRate=InvoiceTotal/VATTotal

    ID=db.Column(db.Integer,primary_key=True)
    Date=db.Column(db.DateTime,nullable=False)
    UploadDate=db.Column(db.DateTime,nullable=False,default=datetime.datetime.now())
    VKN=db.Column(db.String(11),nullable=False)
    InvoiceNumber=db.Column(db.String(100),nullable=False)
    CompanyCode=db.Column(db.String(110),nullable=False)
    VATRate=db.Column(db.Integer,nullable=False)
    VATTotal=db.Column(db.Integer,nullable=False)
    InvoiceTotal=db.Column(db.Integer,nullable=False)
    CategoryID=db.Column(db.Integer,db.ForeignKey(Category.ID),nullable=False)
    UserID=db.Column(db.Integer,db.ForeignKey(User.ID),nullable=False)

    