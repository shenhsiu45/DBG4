from flask import Blueprint, request, redirect, url_for, current_app, render_template, flash

update_bp = Blueprint('update_bp', __name__)

# 更新訂單
@update_bp.route('/update_order/<int:order_id>', methods=['GET', 'POST'])
def update_order(order_id):
    connection = current_app.config['get_db_connection']()
    cursor = connection.cursor(dictionary=True)

    # 查找當前訂單
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
    WHERE o.id = %s
    GROUP BY o.id
    """
    cursor.execute(query, (order_id,))
    order = cursor.fetchone()

    # 處理訂單項目
    if order and order['items']:
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
    elif order:
        order['items'] = []

    if request.method == 'POST':
        # 取得更新的訂單狀態和價格
        new_status = request.form.get('order_status')
        new_price = request.form.get('price')

        # 更新訂單
        update_query = "UPDATE orders SET order_status = %s, total_price = %s WHERE id = %s"
        cursor.execute(update_query, (new_status, float(new_price), order_id))
        connection.commit()

        flash('訂單已更新')

        # 更新後重定向到訂單頁面
        cursor.close()
        connection.close()
        return redirect(url_for('read_bp.view_orders'))

    cursor.close()
    connection.close()

    # 顯示更新訂單的表單
    return render_template('update_order.html', order=order)
