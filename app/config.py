import os
import binascii


class Config:
    SECRET_KEY = binascii.b2a_hex(os.urandom(15))
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/my-port'
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_CODE_THEME = "default"
    
