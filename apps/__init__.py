import logging

from flask import Flask

from exts import login_manager, db, moment, logger, handler, formatter
from settings import Config
from apps.student.views import student_bp
from apps.main.views import main_bp


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    logging.basicConfig(filename='log.txt', filemode='a', level=logging.WARNING,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logger.setLevel(level=logging.WARNING)
    logger.setLevel(level=logging.DEBUG)

    # handler.setLevel(level=logging.INFO)
    handler.setLevel(level=logging.DEBUG)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    login_manager.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    db.create_all(app=app)
    app.register_blueprint(student_bp)
    app.register_blueprint(main_bp)

    return app