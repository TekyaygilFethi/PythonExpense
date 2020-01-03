import flask_sqlalchemy
from IdeconOCRGeneric import db
from sqlalchemy_serializer import SerializerMixin

class Category(db.Model,SerializerMixin):
    __tablename__="CategoryTable"

    def __init__(self, CategoryName):
        self.CategoryName=CategoryName

    ID=db.Column(db.Integer,primary_key=True)
    CategoryName=db.Column(db.String(100),index=True,nullable=False)
    # Invoices=db.relationship('invoicetable',backref='category',lazy=True)

   