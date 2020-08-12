class Configuration(object):
  DEBUG = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  SECRET_KEY = 'YOUR HEAD ASPLODE!'

  # database settings
  DB_USER = "<YOU DB USER>"
  DB_PASSWORD = "<DB PASSWORD>"
  DB_NAME = "<YOUR DB HERE>"
  DB_PROTOCOLS = "mysql+pymysql"
  DB_URI = "<YOUR DB URI>"
  DB_PORT = 3306
  SQLALCHEMY_DATABASE_URI = f"{DB_PROTOCOLS}://{DB_USER}:{DB_PASSWORD}@{DB_URI}:{DB_PORT}/{DB_NAME}"