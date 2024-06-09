from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 连接到MySQL数据库
mysql_conn = mysql.connector.connect(
    host='LAPTOP-KE',
    user='root',
    password='Zhangke123',
)
mysql_cursor = mysql_conn.cursor()
# 创建数据库
mysql_cursor.execute("CREATE DATABASE IF NOT EXISTS user")
mysql_conn.commit()

# 切换到用户数据库
mysql_cursor.execute("USE user")

# 创建用户表
mysql_cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, risk INT, fund FLOAT)")
mysql_conn.commit()
# 注册用户
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        risk_level = data.get('risk_level')
        fund = data.get('initial_fund')
    except Exception as e:
        return jsonify({'error': 'Invalid JSON format'}), 400

    # 检查用户名是否已存在
    mysql_cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = mysql_cursor.fetchone()
    if user:
        return jsonify({'message': 'Username already exists'}), 400

    # 对密码进行哈希处理后存储
    hashed_password = generate_password_hash(password)
    mysql_cursor.execute("INSERT INTO users (username, password, risk, fund) VALUES (%s, %s, %s, %s)", (username, hashed_password, risk_level, fund))
    mysql_conn.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# 用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 获取用户信息
    mysql_cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = mysql_cursor.fetchone()

    if user and check_password_hash(user[2], password):  # 检查密码是否匹配
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# 用户设置
@app.route('/set',methods=['POST'])
def set():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        risk_level = data.get('risk_level')
        fund = data.get('update_fund')
    except Exception as e:
        return jsonify({'error': 'Invalid JSON format'}), 400

    # 获取用户信息
    mysql_cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = mysql_cursor.fetchone()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    # 更新用户信息
    if password:
        hashed_password = generate_password_hash(password)
        mysql_cursor.execute("UPDATE users SET password=%s WHERE username=%s", (hashed_password, username))

    if risk_level:
        mysql_cursor.execute("UPDATE users SET risk=%s WHERE username=%s", (risk_level, username))

    if fund:
        mysql_cursor.execute("UPDATE users SET fund=%s WHERE username=%s", (fund, username))

    mysql_conn.commit()

    return jsonify({'message': 'User information updated successfully'}), 200

if __name__ == '__main__':
    app.run()
