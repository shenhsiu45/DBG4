from flask import Blueprint, request, redirect, url_for
import mysql.connector
from datetime import datetime

# 定義 Blueprint
create_bp = Blueprint('create_bp', __name__)

db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'db'
}

# 新增數據的路由
@create_bp.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('name')

    if name:
        # 連接到 MySQL 數據庫
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # 獲取當前時間
        submission_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_query = "INSERT INTO users (name, created_at) VALUES (%s, %s)"
        cursor.execute(insert_query, (name, submission_time))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for('read_bp.index'))
