from flask import Blueprint, request, redirect, url_for, render_template, current_app ,flash
from bson import ObjectId

from datetime import datetime

create_bp = Blueprint('create_bp', __name__)

@create_bp.route('/add_menu', methods=['GET', 'POST'])
def add_menu_item():
    item_id = request.args.get('item_id')  # 如果是更新操作，獲取 item_id
    if item_id:
        # 如果有 item_id，則表示是更新操作
        try:
            object_id = ObjectId(item_id)
        except Exception:
            return "Invalid ID format", 400
        
        menu_item = current_app.config['restaurant']['menu'].find_one({"_id": object_id})
        if not menu_item:
            return "Item not found", 404
    else:
        menu_item = None  # 如果是新增操作，則 menu_item 為 None

    if request.method == 'POST':
        item_name = request.form.get('name')
        price = request.form.get('price')

        if item_id:
            # 更新操作
            current_app.config['restaurant']['menu'].update_one(
                {"_id": ObjectId(item_id)},
                {"$set": {"name": item_name, "price": float(price)}}
            )
        else:
            # 新增操作
            current_app.config['restaurant']['menu'].insert_one({
                'name': item_name,
                'price': float(price),
                'created_at': datetime.now()
            })
        
        return redirect(url_for('create_bp.add_menu_item'))  # 返回到菜單編輯頁面

    # 獲取所有菜單項目
    menu_items = list(current_app.config['restaurant']['menu'].find())
    for item in menu_items:
        item['_id'] = str(item['_id'])  # 將 _id 轉換為字符串，方便顯示
    
    return render_template('add_menu.html', item=menu_item, results=menu_items)  # 傳遞菜單項目列表


@create_bp.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        item_ids = request.form.getlist('item_id')
        quantities = request.form.getlist('quantity')

        if not item_ids:
            flash('請選擇至少一個餐點')
            return redirect(url_for('create_bp.add_order'))

        # 计算订单总价
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

        # 保存订单到数据库
        new_order = {
            'customer_name': customer_name,
            'items': order_items,
            'total_price': total_price,
            'order_status': 'Pending',
            'created_at': datetime.utcnow()
        }
        orders_collection = current_app.config['restaurant']['orders']
        orders_collection.insert_one(new_order)
        flash('訂單已成功添加')
        return redirect(url_for('read_bp.view_orders'))

    # 获取菜单项
    menu_items = list(current_app.config['restaurant']['menu'].find())
    for item in menu_items:
        item['_id'] = str(item['_id'])
    return render_template('add_order.html', menu_items=menu_items)
