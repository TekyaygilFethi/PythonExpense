import flask_sqlalchemy
from IdeconOCRGeneric import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model,SerializerMixin):
    __tablename__="UserTable"
    
    ID=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(20),nullable=False)
    Surname=db.Column(db.String(30),nullable=False)
    Username=db.Column(db.String(20),index=True,unique=True,nullable=False)
    Password=db.Column(db.String(200),nullable=False)


    def __str__(self):
        return r'{"ID":self.ID,"Name":self.Name,"Surname":self.Surname,"Username":self.Username,"Password":self.Password}'

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}   

