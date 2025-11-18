from flask import Flask
from dotenv import load_dotenv
import os
import pymysql
import matplotlib
matplotlib.use('Agg')

load_dotenv()

app = Flask(__name__)

# conexão MYSQL
def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT')),
        cursorclass=pymysql.cursors.DictCursor
    )

# Importa rotas
from routes import *

if __name__ == '__main__':
    app.run(debug=True)