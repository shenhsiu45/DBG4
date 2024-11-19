from flask import Blueprint, request, redirect, url_for, render_template, current_app ,flash
from bson import ObjectId

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
            # 插入到 MongoDB 餐點集合
            current_app.config['restaurant']['menu'].insert_one({
                'name': item_name,
                'price': float(price),
                'created_at': datetime.now()
            })

            return redirect(url_for('read_bp.view_menu'))
    return render_template('add_menu.html')

@create_bp.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        item_ids = request.form.getlist('item_id')  # 多选支持
        quantities = request.form.getlist('quantity')  # 每项的数量
        orders_collection = current_app.config['restaurant']['orders']

        # 檢查是否有選擇餐點
        if not item_ids:
            flash('請選擇至少一個餐點')
            return redirect(url_for('create_bp.add_order'))

        # 計算訂單總價
        order_items = []
        total_price = 0
        for item_id, quantity in zip(item_ids, quantities):
            menu_item = current_app.config['restaurant']['menu'].find_one({"_id": ObjectId(item_id)})
            if menu_item:
                item_price = float(menu_item['price'])
                quantity = int(quantity)
                total_price += item_price * quantity
                order_items.append({
                    'item_id': item_id,
                    'name': menu_item['name'],
                    'quantity': quantity,
                    'price': item_price
                })

        # 保存訂單到資料庫
        new_order = {
        'customer_name': customer_name,
        'items': order_items,
        'total_price': total_price,
        'order_status': 'Pending',
        'created_at': datetime.utcnow()
        }
        orders_collection.insert_one(new_order)
        flash('訂單已成功添加')
        return redirect(url_for('read_bp.view_orders'))

    # 載入所有餐點
    menu_items = list(current_app.config['restaurant']['menu'].find())
    for item in menu_items:
        item['_id'] = str(item['_id'])  # 轉換 _id 為字符串
    return render_template('add_order.html', menu_items=menu_items)

