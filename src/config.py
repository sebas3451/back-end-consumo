from dotenv import load_dotenv
import os

load_dotenv()

user =os.environ['MYSQL_USER']
database = os.environ['MYSQL_DATABASE']
password = os.environ['MYSQL_PASSWORD']
host = os.environ['MYSQL_HOST']
port = os.environ['MYSQL_PORT']

SECRET_KEY = os.environ['SECRET_KEY']
DATABASE_CONNECTION_URI = f'mysql://{user}:{password}@{host}:{port}/{database}'