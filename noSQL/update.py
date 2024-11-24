from flask import Blueprint, request, redirect, url_for, current_app, render_template,flash
from bson.objectid import ObjectId

update_bp = Blueprint('update_bp', __name__)

# 更新訂單
@update_bp.route('/update_order/<order_id>', methods=['GET', 'POST'])
def update_order(order_id):
    # 查找當前訂單
    order = current_app.config['restaurant']['orders'].find_one({'_id': ObjectId(order_id)})

    if request.method == 'POST':
        # 取得更新的訂單狀態和價格
        new_status = request.form.get('order_status')
        new_price = request.form.get('price')

        # 更新訂單
        if new_price:
            current_app.config['restaurant']['orders'].update_one(
                {'_id': ObjectId(order_id)},
                {'$set': {'order_status': new_status, 'total_price': float(new_price)}}  # 確保價格是浮點數
            )
        flash('訂單已更新')

        # 更新後重定向到訂單頁面
        return redirect(url_for('read_bp.view_orders'))

    # 顯示更新訂單的表單
    return render_template('orders.html', order=order)

@update_bp.route('/update/<item_id>', methods=['GET', 'POST'])
def update_menu_item(item_id):
    try:
        object_id = ObjectId(item_id)
    except Exception:
        return "Invalid ID format", 400

    # 查找菜單項目
    menu_item = current_app.config['restaurant']['menu'].find_one({"_id": object_id})
    if not menu_item:
        return "Item not found", 404

    if request.method == 'POST':
        # 更新菜單項目
        new_name = request.form.get('name')
        new_price = float(request.form.get('price'))
        current_app.config['restaurant']['menu'].update_one(
            {"_id": object_id},
            {"$set": {"name": new_name, "price": new_price}}
        )
        return redirect(url_for('read_bp.view_menu'))

    return render_template('add_menu.html', item=menu_item)
