from flask import Blueprint, request, render_template, current_app

search_bp = Blueprint('search_bp', __name__)

# 搜索餐點
@search_bp.route('/search_menu', methods=['GET', 'POST'])
def search_menu():
    connection = current_app.config['get_db_connection']()
    cursor = connection.cursor(dictionary=True)

    # 預設顯示所有餐點
    query = "SELECT id, name, price, created_at FROM menu"
    cursor.execute(query)
    menu_items = cursor.fetchall()

    results = menu_items  # 預設結果為所有餐點
    search_query = ""

    if request.method == 'POST':
        search_query = request.form.get('query')
        if search_query:
            # 搜索餐點名稱中包含關鍵字的項目 (忽略大小寫)
            search_query_sql = "SELECT id, name, price, created_at FROM menu WHERE name LIKE %s"
            cursor.execute(search_query_sql, (f"%{search_query}%",))
            results = cursor.fetchall()

    cursor.close()
    connection.close()

    # 傳遞所有餐點和搜索結果到模板
    return render_template('menu.html', menu_items=menu_items, results=results, query=search_query)

# 搜索訂單
@search_bp.route('/search_order', methods=['GET', 'POST'])
def search_order():
    connection = current_app.config['get_db_connection']()
    cursor = connection.cursor(dictionary=True)

    # 預設顯示所有訂單
    query = """
    SELECT 
        o.id AS order_id, 
        o.customer_name, 
        o.total_price, 
        o.order_status, 
        o.created_at,
        GROUP_CONCAT(CONCAT(oi.menu_id, ':', oi.quantity, ':', oi.price) SEPARATOR '|') AS items
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    GROUP BY o.id
    """
    cursor.execute(query)
    orders = cursor.fetchall()

    results = orders  # 預設結果為所有訂單
    search_query = ""

    if request.method == 'POST':
        search_query = request.form.get('query')
        if search_query:
            # 搜索訂單顧客名稱中包含關鍵字的訂單 (忽略大小寫)
            search_query_sql = """
            SELECT 
                o.id AS order_id, 
                o.customer_name, 
                o.total_price, 
                o.order_status, 
                o.created_at,
                GROUP_CONCAT(CONCAT(oi.menu_id, ':', oi.quantity, ':', oi.price) SEPARATOR '|') AS items
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE o.customer_name LIKE %s
            GROUP BY o.id
            """
            cursor.execute(search_query_sql, (f"%{search_query}%",))
            results = cursor.fetchall()

    # 處理訂單項目以便於前端顯示
    for order in results:
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

    # 傳遞所有訂單和搜索結果到模板
    return render_template('orders.html', orders=orders, results=results, query=search_query)
