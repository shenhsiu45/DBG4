from flask import Blueprint, request, redirect, url_for
import mysql.connector

# 定義 Blueprint
delete_bp = Blueprint('delete_bp', __name__)

db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'db'
}

@delete_bp.route('/delete', methods=['POST'])
def delete_user():
    user_ids = request.form.getlist('user_ids')  # 獲取所有選中的用戶ID

    if user_ids:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 創建一個 SQL DELETE 語句來刪除所有選中的用戶
        delete_query = "DELETE FROM users WHERE id IN (%s)" % ','.join(['%s'] * len(user_ids))
        cursor.execute(delete_query, tuple(user_ids))
        conn.commit()

        cursor.close()
        conn.close()

    return redirect(url_for('read_bp.index'))  # 返回到用戶列表頁面
