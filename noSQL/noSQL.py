from flask import Flask, render_template
from pymongo import MongoClient

from create import create_bp
from read import read_bp
from delete import delete_bp
from update import update_bp
from search import search_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 設定一個唯一且隨機的秘鑰

import os
app.secret_key = os.urandom(24)  # 生成一個隨機的 24 字元字串作為 secret_key

# MongoDB 連接（根據你的本地設置進行調整）
client = MongoClient('mongodb://localhost:27017/')
db = client['local']  # 數據庫名稱

# 將 db 作為全局變量，以便在 Blueprint 中使用
app.config['restaurant'] = db

# 註冊 Blueprint，並為每個 Blueprint 設置唯一的 url_prefix
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
