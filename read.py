from flask import Blueprint, render_template
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
    menu_items = list(menu_collection.find())
    for item in menu_items:
        item['_id'] = str(item['_id'])  # 转换 _id 为字符串便于显示
    return render_template('menu.html', menu_items=menu_items)

# 查看所有訂單
@read_bp.route('/orders')
def view_orders():
    orders = list(orders_collection.find())
    for order in orders:
        order['_id'] = str(order['_id'])  # 转换 _id 为字符串便于显示
    return render_template('orders.html', orders=orders)



