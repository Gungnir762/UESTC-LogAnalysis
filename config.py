"""
author:zyr
function:数据库连接的配置文件
notice:None
"""
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'forensicsdb'
USERNAME = 'root'
PASSWORD = '123'
SQLALCHEMY_DATABASE_URI = rf'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
