from flask import Blueprint, request, render_template
import mysql.connector

# 定义 Blueprint
search_bp = Blueprint('search_bp', __name__)

db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'db'
}

# 搜索用户的路由
@search_bp.route('/search', methods=['GET'])
def search_user():
    search_query = request.args.get('query', '')  # 从URL中获取搜索查询参数

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 使用LIKE语句来查找与查询匹配的用户名
    search_query = "%" + search_query + "%"
    search_query_sql = "SELECT * FROM users WHERE name LIKE %s"
    cursor.execute(search_query_sql, (search_query,))
    search_results = cursor.fetchall()

    cursor.close()
    conn.close()

    # 渲染包含搜索结果的页面
    return render_template('index.html', users=search_results)

# 搜索产品的路由
@search_bp.route('/search_product', methods=['GET'])
def search_product():
    search_query = request.args.get('query', '')  # 从URL中获取搜索查询参数

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # 使用LIKE语句来查找与查询匹配的产品名
    search_query = "%" + search_query + "%"
    search_query_sql = "SELECT * FROM product WHERE name LIKE %s"
    cursor.execute(search_query_sql, (search_query,))
    search_results = cursor.fetchall()

    cursor.close()
    conn.close()

    # 渲染包含搜索结果的页面
    return render_template('index.html', products=search_results)
