import sqlite3
import os

# 数据库文件路径
db_path = os.path.join(os.path.dirname(__file__), '..', 'numa.db')

def init_db():
    # 连接到数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建applications表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            repository_url TEXT,
            status TEXT DEFAULT 'created',
            development_task_id INTEGER,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            built_at TIMESTAMP,
            FOREIGN KEY (development_task_id) REFERENCES development_tasks (id),
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("Applications table created successfully.")

if __name__ == "__main__":
    init_db()