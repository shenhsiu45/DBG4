from flask import Blueprint, request, render_template, current_app

search_bp = Blueprint('search_bp', __name__)

# 搜索餐點
@search_bp.route('/search_menu', methods=['GET', 'POST'])
def search_menu():
    # 預設顯示所有餐點
    menu_items = list(current_app.config['restaurant']['menu'].find())
    results = menu_items  # 預設結果為所有餐點
    query = ""

    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # 搜索餐點名稱中包含關鍵字的項目 (忽略大小寫)
            results = list(current_app.config['restaurant']['menu'].find({"name": {"$regex": query, "$options": "i"}}))
            for item in results:
                item['_id'] = str(item['_id'])  # 將 _id 轉換為字符串以便於顯示

    # 傳遞所有餐點和搜索結果到模板
    return render_template('menu.html', menu_items=menu_items, results=results, query=query)

# 搜索訂單
@search_bp.route('/search_order', methods=['GET', 'POST'])
def search_order():
    orders = list(current_app.config['restaurant']['orders'].find())
    for order in orders:
        order['_id'] = str(order['_id'])

    results = orders  # 默認顯示所有訂單
    query = ""

    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # 搜索訂單顧客名稱中包含關鍵字的訂單 (忽略大小寫)
            results = list(current_app.config['restaurant']['orders'].find({"customer_name": {"$regex": query, "$options": "i"}}))
            for order in results:
                order['_id'] = str(order['_id'])

    return render_template('orders.html', orders=orders, results=results, query=query)

