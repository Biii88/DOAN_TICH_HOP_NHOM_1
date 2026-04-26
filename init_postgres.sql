-- Dành riêng cho PostgreSQL
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Thêm dữ liệu mẫu để báo cáo có cái để hiển thị
INSERT INTO transactions (order_id, status) VALUES 
(100, 'SUCCESS'), 
(101, 'PENDING'), 
(102, 'FAILED');