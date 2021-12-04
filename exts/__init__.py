import logging

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

#from model import User

login_manager = LoginManager()
db = SQLAlchemy()
moment = Moment()
logger = logging.getLogger('app')
handler = logging.FileHandler("log.txt")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@login_manager.user_loader
def load_user(user_id):
    from model import User
    user = User.query.get(int(user_id))
    return user
