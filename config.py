import os

class Config:
    KEY_db=os.getenv('KEY')
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:{KEY_db}@localhost:5432/data_base"
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
