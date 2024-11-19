from flask import Flask, render_template
import mysql.connector
from create import create_bp
from read import read_bp
from delete import delete_bp
from update import update_bp
from search import search_bp

app = Flask(__name__)

# 設置隨機秘鑰
import os
app.secret_key = os.urandom(24)

# MySQL 資料庫連接
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',  # 修改為你的 MySQL 使用者名稱
        password='password',  # 修改為你的 MySQL 密碼
        database='restaurant'  # 修改為你的資料庫名稱
    )

# 將資料庫連接函數加入配置
app.config['get_db_connection'] = get_db_connection

# 註冊 Blueprint
app.register_blueprint(create_bp, url_prefix='/create')
app.register_blueprint(read_bp, url_prefix='/read')
app.register_blueprint(delete_bp, url_prefix='/delete')
app.register_blueprint(update_bp, url_prefix='/update')
app.register_blueprint(search_bp, url_prefix='/search')

# 添加首頁路由
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
