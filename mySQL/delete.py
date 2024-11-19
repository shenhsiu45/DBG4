from flask import Blueprint, redirect, url_for, current_app

delete_bp = Blueprint('delete_bp', __name__)

# 刪除訂單
@delete_bp.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    connection = current_app.config['get_db_connection']()
    cursor = connection.cursor()

    try:
        # 刪除訂單明細（order_items 表中與該訂單相關的資料）
        delete_order_items_query = "DELETE FROM order_items WHERE order_id = %s"
        cursor.execute(delete_order_items_query, (order_id,))

        # 刪除訂單（orders 表中的資料）
        delete_order_query = "DELETE FROM orders WHERE id = %s"
        cursor.execute(delete_order_query, (order_id,))

        # 確保資料庫變更提交
        connection.commit()

        # 如果刪除的訂單數為 0，則表示該訂單不存在
        if cursor.rowcount == 0:
            return "Order not found", 404
    except Exception as e:
        connection.rollback()
        return f"An error occurred: {e}", 500
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('read_bp.view_orders'))
