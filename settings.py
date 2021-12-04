class Config:
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:zktj1016@127.0.0.1:3306/school'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # secret_key
    SECRET_KEY = 'random_key'