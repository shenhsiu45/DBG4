from flask import Blueprint, render_template
import mysql.connector

# 定義 Blueprint
read_bp = Blueprint('read_bp', __name__)

db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'db'
}

@read_bp.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 查詢用戶
    select_user_query = "SELECT * FROM users"
    cursor.execute(select_user_query)
    users = cursor.fetchall()

    # 查詢產品
    select_product_query = "SELECT * FROM product"
    cursor.execute(select_product_query)
    products = cursor.fetchall()

    # 查詢order
    select_order_query = "SELECT * FROM orders"
    cursor.execute(select_order_query)
    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    # Render the posts with the add/delete functionality
    return render_template('index.html', orders=orders, users=users, products=products)
