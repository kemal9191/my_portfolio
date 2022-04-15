import os
import binascii

database_filename = "portfolio"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "postgresql://{}".format(os.path.join(project_dir, database_filename))

class Config:
    SECRET_KEY = binascii.b2a_hex(os.urandom(15))
    SQLALCHEMY_DATABASE_URI = database_path
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = "default"
    
