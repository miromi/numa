import sqlite3

# 连接到数据库
conn = sqlite3.connect('/Users/yao/source/numa/numa_backend/numa.db')
cursor = conn.cursor()

# 手动更新需求状态
cursor.execute("UPDATE requirements SET status = 'confirmed' WHERE id = 2")
conn.commit()

# 验证更新
cursor.execute("SELECT id, title, status, clarified FROM requirements WHERE id = 2")
result = cursor.fetchone()
print(f"需求ID: {result[0]}, 标题: {result[1]}, 状态: {result[2]}, 已澄清: {result[3]}")

# 关闭连接
conn.close()