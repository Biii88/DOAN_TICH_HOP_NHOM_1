import pandas as pd
import mysql.connector
import os, shutil, time

def run_adapter():
    input_file = "/app/input/inventory.csv"
    processed_path = "/app/processed/inventory_done.csv"

    while True:
        if os.path.exists(input_file):
            print("--- Phát hiện file inventory.csv của Nhóm 1 ---")
            try:
                # 1. Đọc dữ liệu
                df = pd.read_csv(input_file)
                
                # 2. Kết nối Database
                conn = mysql.connector.connect(host="mysql-db", user="root", password="root", database="web_store")
                cursor = conn.cursor()

                success_count = 0
                error_count = 0

                # 3. Duyệt từng dòng để xử lý lỗi NEGATIVE_NUMBERS
                for _, row in df.iterrows():
                    try:
                        p_id = int(row['product_id'])
                        qty = int(row['quantity'])

                        if qty < 0:
                            print(f"[CẢNH BÁO] Bỏ qua Product {p_id} vì tồn kho âm: {qty}")
                            error_count += 1
                            continue
                        
                        # Cập nhật vào bảng products (lưu ý tên cột trong init.sql là 'stock')
                        cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (qty, p_id))
                        success_count += 1
                    except Exception as row_error:
                        print(f"Lỗi dòng dữ liệu: {row_error}")
                        error_count += 1
                
                conn.commit()
                conn.close()

                # 4. Di chuyển file sau khi xử lý xong
                shutil.move(input_file, processed_path)
                print(f"--- HOÀN THÀNH: Thành công {success_count}, Lỗi {error_count} ---")

            except Exception as e:
                print(f"Lỗi hệ thống: {e}")
        
        time.sleep(10)

run_adapter()