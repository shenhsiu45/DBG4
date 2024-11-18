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
