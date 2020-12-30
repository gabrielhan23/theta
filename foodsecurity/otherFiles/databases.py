from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import uuid

from otherFiles.setup import app

db = SQLAlchemy(app)

#TIER ONE DATABASE
class Store(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    #information
    username = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    addressNum = db.Column(db.Integer, nullable=False)
    addressStreet = db.Column(db.String(50), nullable=False)
    addressCity = db.Column(db.String(50), nullable=False)
    zipCode = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    items = db.relationship('Item', backref='store', lazy=True)
    #listings = db.Column
    #return
    def __repr__(self):
        return "Store("+self.username+", "+self.name+")"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #information
    uuid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    sellBy = db.Column(db.Date, nullable=False)
    expiration = db.Column(db.Date, nullable=False)
    pickupTime = db.Column(db.String(50), nullable=True)
    customer_name = db.Column(db.String(50), nullable=True)

    img_directory = db.Column(db.Text, nullable=True, default="default.jpg")
    
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=True)

    pickupTimes = db.relationship('Pickup', backref='item', lazy=True)

    #return
    def __repr__(self):
        return "Item("+self.name+", "+self.uuid+")"

class Pickup(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #information
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    #return
    def __repr__(self):
        return "Pickup("+str(self.start)+", "+str(self.end)+")"



db.create_all()