from flask import Blueprint, redirect, url_for, current_app
from bson.objectid import ObjectId

delete_bp = Blueprint('delete_bp', __name__)

# 刪除訂單
@delete_bp.route('/delete_order/<order_id>', methods=['POST'])
def delete_order(order_id):
    # 嘗試刪除指定的訂單
    result = current_app.config['restaurant']['orders'].delete_one({'_id': ObjectId(order_id)})

    # 如果沒有找到匹配的訂單
    if result.deleted_count == 0:
        return "Order not found", 404

    return redirect(url_for('read_bp.view_orders'))

@delete_bp.route('/delete/<item_id>', methods=['POST'])
def delete_menu_item(item_id):
    try:
        object_id = ObjectId(item_id)
    except Exception:
        return "Invalid ID format", 400

    result = current_app.config['restaurant']['menu'].delete_one({"_id": object_id})
    if result.deleted_count == 0:
        return "Item not found", 404

    return redirect(url_for('read_bp.view_menu'))
