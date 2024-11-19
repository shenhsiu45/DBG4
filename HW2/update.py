from flask import Blueprint, request, redirect, url_for
import mysql.connector

# 定义 Blueprint
update_bp = Blueprint('update_bp', __name__)

db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'db'
}

# 更新用户的路由
@update_bp.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    # 获取表单中的所有字段
    form_data = request.form.to_dict()

    # 提取当前用户的 name 字段 (例如：name-1, name-2, ...)
    new_name = form_data.get(f'name-{user_id}')

    # 检查是否有输入新名字
    if not new_name:
        return "No name provided", 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 更新用户名字
    update_query = "UPDATE users SET name = %s WHERE id = %s"
    cursor.execute(update_query, (new_name, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))

# 更新订单的路由
@update_bp.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    # 获取表单中的所有字段
    form_data = request.form.to_dict()

    # 提取订单中可能需要更新的字段
    new_quantity = form_data.get(f'quantity-{order_id}')
    new_total_price = form_data.get(f'total_price-{order_id}')

    # 检查是否输入了新的数量或价格
    if not new_quantity or not new_total_price:
        return "Quantity or total price not provided", 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # 更新订单数量和总价格
    update_query = "UPDATE orders SET Quantity = %s, Total_price = %s WHERE id = %s"
    cursor.execute(update_query, (new_quantity, new_total_price, order_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('read_bp.index'))
