from flask import Flask



app = Flask(__name__)



from app.init import initApp
from app.user import user_register, user_login,change_password,recover_password
from app.patient import create,search, update, delete
from app.email import  send_email

