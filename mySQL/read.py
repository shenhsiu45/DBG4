from flask import Blueprint, render_template, current_app

# 定義 Blueprint
read_bp = Blueprint('read_bp', __name__)

# 查看所有餐點
@read_bp.route('/menu')
def view_menu():
    connection = current_app.config['get_db_connection']()
    cursor = connection.cursor(dictionary=True)

    # 從 `menu` 表中獲取所有餐點
    query = "SELECT id, name, price, created_at FROM menu"
    cursor.execute(query)
    menu_items = cursor.fetchall()

    cursor.close()
    connection.close()

    # 傳遞餐點資料到模板
    return render_template('menu.html', menu_items=menu_items)

# 查看所有訂單
@read_bp.route('/orders')
def view_orders():
    connection = current_app.config['get_db_connection']()
    cursor = connection.cursor(dictionary=True)

    # 从 `orders` 表中获取所有订单
    query = """
    SELECT 
        o.id AS order_id,
        o.customer_name,
        o.total_price,
        o.order_status,
        o.created_at,
        GROUP_CONCAT(
            CONCAT( oi.quantity, ':', oi.price)
            SEPARATOR '|'
        ) AS items
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    GROUP BY o.id, o.customer_name, o.total_price, o.order_status, o.created_at;
    """
    cursor.execute(query)
    orders = cursor.fetchall()

    # 处理订单项目以便于前端显示
    for order in orders:
        if order['items']:  # 确保 items 不为 None
            order_items = []
            items_data = order['items'].split('|')  # 将 items 分割成各个项目
            for item_data in items_data:
                try:
                    menu_id, quantity, price = item_data.split(':')  # 分割出 menu_id, quantity, price
                    order_items.append({
                        'menu_id': int(menu_id),  # 解析 menu_id
                        'quantity': int(quantity),  # 解析数量
                        'price': float(price)  # 解析价格
                    })
                except (ValueError, TypeError):
                    continue  # 跳过错误数据
            order['items'] = order_items
        else:
            order['items'] = []  # 如果 items 为 None 或空字符串，设置为空列表


    cursor.close()
    connection.close()

    # 传递订单数据到模板
    return render_template('orders.html', orders=orders)
