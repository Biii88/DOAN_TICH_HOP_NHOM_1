from fastapi import FastAPI, HTTPException
import pymysql
import psycopg2

app = FastAPI()

# 1. BỎ VÒNG LẶP ĐỂ THẤY LỖI THỰC SỰ
def connect_mysql():
    try:
        return pymysql.connect(
            host="mysql-db",
            user="root",
            password="root",
            database="web_store",
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        # In thẳng lỗi ra log để debug
        print(f"Lỗi kết nối MySQL: {e}")
        raise e 

def connect_postgres():
    try:
        return psycopg2.connect(
            host="postgres",
            user="postgres",
            password="123",
            dbname="finance"
        )
    except Exception as e:
        print(f"Lỗi kết nối Postgres: {e}")
        raise e

@app.get("/api/report")
def get_report(page: int = 1, limit: int = 50):
    offset = (page - 1) * limit
    
    # Nếu kết nối có lỗi, code sẽ crash ngay lập tức và trả về lỗi 500 thay vì treo
    try:
        db_mysql = connect_mysql()
        cursor_mysql = db_mysql.cursor()
        cursor_mysql.execute(f"SELECT id, user_id, total_price, status FROM orders LIMIT {limit} OFFSET {offset}")
        orders = cursor_mysql.fetchall()
        db_mysql.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MySQL Error: {str(e)}")

    if not orders:
        return {"data": [], "message": "No orders found"}

    try:
        db_pg = connect_postgres()
        cursor_pg = db_pg.cursor()
        
        order_ids = tuple([o['id'] for o in orders])
        if len(order_ids) == 1:
            query_pg = f"SELECT order_id, status FROM transactions WHERE order_id = {order_ids[0]}"
            cursor_pg.execute(query_pg)
        else:
            query_pg = "SELECT order_id, status FROM transactions WHERE order_id IN %s"
            cursor_pg.execute(query_pg, (order_ids,))
            
        transactions = cursor_pg.fetchall()
        db_pg.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Postgres Error: {str(e)}")

    tx_map = {tx[0]: tx[1] for tx in transactions}
    for order in orders:
        order['finance_status'] = tx_map.get(order['id'], "PENDING")

    return {"page": page, "data": orders}