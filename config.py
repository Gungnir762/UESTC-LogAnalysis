HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'forensicsdb'
USERNAME = 'zyr'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# DB_URI = 'mysql+pymysql://root:Zyr123456@@localhost:3306/stargallery?charset=utf8'
SQLALCHEMY_DATABASE_URI = DB_URI

# SQLALCHEMY_TRACK_MODIFICATIONS = True

# SECRET_KEY = "123456"
