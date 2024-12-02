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

@create_bp.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        # 從表單獲取數據
        customer_name = request.form.get('customer_name')
        item_id = request.form.getlist('item_id')  # 餐點 ID 列表
        quantities = request.form.getlist('quantity')  # 對應的數量列表

        # 驗證輸入
        if not item_id or not customer_name:
            flash('請輸入顧客名稱並選擇至少一個餐點')
            return redirect(url_for('create_bp.add_order'))

        # 建立資料庫連線
        db = current_app.config['get_db_connection']()
        cursor = db.cursor()

        try:
            # 初始化總價和訂單項目列表
            total_price = 0
            order_items = []

            # 從 menu 表中獲取每個餐點的詳細資訊，並計算總價
            for item_id, quantity in zip(item_id, quantities):
                cursor.execute("SELECT id, name, price FROM menu WHERE id = %s", (item_id,))
                menu_item = cursor.fetchone()

                if not menu_item:
                    flash('所選餐點無效或已刪除')
                    return redirect(url_for('create_bp.add_order'))

                menu_id, item_name, item_price = menu_item
                quantity = int(quantity)
                item_total_price = float(item_price) * quantity
                total_price += item_total_price

                # 將餐點信息添加到訂單項目列表
                order_items.append({
                    'menu_id': menu_id,
                    'name': item_name,
                    'quantity': quantity,
                    'price': item_price
                })

            # 插入訂單到 orders 表
            cursor.execute(
                """
                INSERT INTO orders (customer_name, total_price, order_status, created_at)
                VALUES (%s, %s, %s, %s)
                """,
                (customer_name, total_price, 'Pending', datetime.utcnow())
            )
            order_id = cursor.lastrowid  # 獲取新插入的訂單 ID

            # 提交更改
            db.commit()
            flash('訂單已成功添加')
            return redirect(url_for('read_bp.view_orders'))

        except Exception as e:
            # 發生錯誤時回滾
            db.rollback()
            print(f"Error: {e}")  # 打印錯誤信息以供調試
            flash('發生錯誤，請稍後再試')
            return redirect(url_for('create_bp.add_order'))

        finally:
            # 關閉游標和資料庫連線
            cursor.close()
            db.close()

    # 如果是 GET 請求，從 menu 表中獲取菜單項目
    db = current_app.config['get_db_connection']()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()  # 獲取所有菜單項目
    cursor.close()
    db.close()

    # 渲染模板，將菜單項目傳遞給前端
    return render_template('add_order.html', menu_items=menu_items)