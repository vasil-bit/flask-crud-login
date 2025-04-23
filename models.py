from extencions import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column (db.String(200), nullable=False)
    
    def __repr__(self):
        return f"<User {self.nombre}>"  
    