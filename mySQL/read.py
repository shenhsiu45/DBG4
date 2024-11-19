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

    # 從 `orders` 表中獲取所有訂單
    query = """
    SELECT 
        o.id AS order_id,
        o.customer_name,
        o.total_price,
        o.order_status,
        o.created_at,
        GROUP_CONCAT(
            CONCAT(oi.menu_id, ':', oi.quantity, ':', oi.price)
            SEPARATOR '|'
        ) AS items
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    GROUP BY o.id
    """
    cursor.execute(query)
    orders = cursor.fetchall()

    # 處理訂單項目以便於前端顯示
    for order in orders:
        if order['items']:
            order_items = []
            items_data = order['items'].split('|')
            for item_data in items_data:
                menu_id, quantity, price = item_data.split(':')
                order_items.append({
                    'menu_id': int(menu_id),
                    'quantity': int(quantity),
                    'price': float(price)
                })
            order['items'] = order_items
        else:
            order['items'] = []

    cursor.close()
    connection.close()

    # 傳遞訂單資料到模板
    return render_template('orders.html', orders=orders)
