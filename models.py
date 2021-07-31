from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PersonModel(db.Model):
    __tablename__ = "table"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer(),unique = True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    age = db.Column(db.Integer())
    cellphone = db.Column(db.Integer)
    address = db.Column(db.String(80))

    def __init__(self,dni,first_name,last_name,age,cellphone,address):
        self.dni = dni
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.cellphone = cellphone
        self.address = address

    def __repr__(self):
        return f"{self.first_name} {self.last_name} | DNI: {self.dni}"