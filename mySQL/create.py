from flask import Blueprint, request, redirect, url_for, render_template, current_app, flash
from datetime import datetime

create_bp = Blueprint('create_bp', __name__)

# 新增餐點的路由
@create_bp.route('/add_menu', methods=['GET', 'POST'])
def add_menu_item():
    if request.method == 'POST':
        # 從表單獲取餐點名稱和價格
        item_name = request.form.get('item_name')
        price = request.form.get('price')

        # 檢查餐點名稱和價格是否提供
        if item_name and price:
            connection = current_app.config['get_db_connection']()
            cursor = connection.cursor()

            # 插入餐點到 MySQL
            query = """
            INSERT INTO menu (name, price, created_at)
            VALUES (%s, %s, %s)
            """
            values = (item_name, float(price), datetime.now())
            cursor.execute(query, values)

            connection.commit()
            cursor.close()
            connection.close()

            flash('餐點已成功添加')
            return redirect(url_for('read_bp.view_menu'))

    return render_template('add_menu.html')

# 新增訂單的路由
@create_bp.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        try:
            # 取得表單數據
            customer_name = request.form.get('customer_name')
            item_ids = request.form.getlist('item_ids')
            quantities = request.form.getlist('quantities')

            # 驗證表單數據
            if not customer_name or not item_ids:
                flash('請輸入顧客名稱並選擇至少一個餐點')
                return redirect(url_for('create_bp.add_order'))

            # 建立資料庫連線
            db = current_app.config['get_db_connection']()
            cursor = db.cursor()

            # 計算訂單總價
            total_price = 0
            order_items = []
            for item_id, quantity in zip(item_ids, quantities):
                cursor.execute("SELECT name, price FROM menu WHERE id = %s", (item_id,))
                menu_item = cursor.fetchone()
                if menu_item:
                    item_name, price = menu_item
                    quantity = int(quantity)
                    total_price += price * quantity
                    order_items.append((item_id, item_name, quantity, price))

            # 插入訂單
            cursor.execute(
                "INSERT INTO orders (customer_name, total_price, order_status, created_at) VALUES (%s, %s, %s, NOW())",
                (customer_name, total_price, 'Pending')
            )
            order_id = cursor.lastrowid

            # 插入訂單詳細項目
            for item_id, item_name, quantity, price in order_items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, item_id, item_name, quantity, price) VALUES (%s, %s, %s, %s, %s)",
                    (order_id, item_id, item_name, quantity, price)
                )

            # 提交更改
            db.commit()
            flash('訂單已成功提交')
            return redirect(url_for('read_bp.view_orders'))

        except Exception as e:
            # 發生錯誤時回滾
            db.rollback()
            print(f"Error: {e}")  # 打印錯誤詳細資訊
            flash('發生錯誤，請稍後再試')
            return redirect(url_for('create_bp.add_order'))

        finally:
            # 關閉資料庫連線
            cursor.close()
            db.close()

    # 載入菜單項目
    db = current_app.config['get_db_connection']()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('add_order.html', menu_items=menu_items)
