from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    laptops = db.relationship('Laptop', backref='brand', lazy=True)

class CPU(db.Model):
    __tablename__ = 'cpu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    laptops = db.relationship('Laptop', backref='cpu', lazy=True)

class GPU(db.Model):
    __tablename__ = 'gpu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    laptops = db.relationship('Laptop', backref='gpu', lazy=True)

class OS(db.Model):
    __tablename__ = 'os'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    laptops = db.relationship('Laptop', backref='os', lazy=True)

class UseCase(db.Model):
    __tablename__ = 'usecase'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(100))
    laptops = db.relationship('Laptop', backref='usecase', lazy=True)

class Laptop(db.Model):
    __tablename__ = 'laptop'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    model = db.Column(db.String(100))
    screensize = db.Column(db.Float)
    cpu_id = db.Column(db.Integer, db.ForeignKey('cpu.id'))
    gpu_id = db.Column(db.Integer, db.ForeignKey('gpu.id'))
    memory = db.Column(db.Integer)
    storage = db.Column(db.Integer)
    os_id = db.Column(db.Integer, db.ForeignKey('os.id'))
    usecase_id = db.Column(db.Integer, db.ForeignKey('usecase.id'))

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_cost = db.Column(db.Float, nullable=False)

class OrderDetails(db.Model):
    __tablename__ = 'order_details'
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    laptop_id = db.Column(db.Integer, db.ForeignKey('laptop.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

