from flask import Blueprint, render_template,current_app
from pymongo import MongoClient

# 定义 Blueprint
read_bp = Blueprint('read_bp', __name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['local']
menu_collection = db['menu']
orders_collection = db['orders']

# 查看所有餐點
@read_bp.route('/menu')
def view_menu():
    # 確保從正確的 MongoDB 集合中獲取菜單項目
    menu_items = list(current_app.config['restaurant']['menu'].find())
    
    # 將每個菜單項目的 _id 轉換為字符串
    for item in menu_items:
        item['_id'] = str(item['_id'])

    return render_template('menu.html', menu_items=menu_items)


# 查看所有訂單
@read_bp.route('/orders')
def view_orders():
    orders = current_app.config['restaurant']['orders'].find()
    orders = [{'_id': str(order['_id']), **order} for order in orders]  # 将 `_id` 转换为字符串
    return render_template('orders.html', orders=orders)




