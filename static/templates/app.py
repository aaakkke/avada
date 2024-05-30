from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# 创建数据库并初始化用户表
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT,risk INTEGER,fund INTEGER)''')
conn.commit()
conn.close()

# 注册用户
@app.route('/register', methods=['POST','GET'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        risk_level = data.get('risk_level')
        fund = data.get('initial_fund')
        print(data)
    except Exception as e:
        return jsonify({'error': 'Invalid JSON format'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # 检查用户名是否已存在
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user:
        conn.close()
        return jsonify({'message': 'Username already exists'}), 400

    # 对密码进行哈希处理后存储
    hashed_password = generate_password_hash(password)
    c.execute("INSERT INTO users (username, password, risk, fund) VALUES (?, ?, ?, ?)", (username, hashed_password,risk_level,fund))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

# 用户登录
@app.route('/login', methods=['POST','GET'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # 获取用户信息
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    if user and check_password_hash(user[2], password):  # 检查密码是否匹配
        conn.close()
        return jsonify({'message': 'Login successful'}), 200
    else:
        conn.close()
        return jsonify({'message': 'Invalid username or password'}), 401

#用户设置:为了实现特定身份验证，用户无法修改用户名
@app.route('/set',methods=['POST','GET'])
def set():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        risk_level = data.get('risk_level')
        fund = data.get('update_fund')
    except Exception as e:
        return jsonify({'error': 'Invalid JSON format'}), 400

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # 获取用户信息
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()

    if not user:
        conn.close()
        return jsonify({'message': 'User not found'}), 404

    # 更新用户信息
    if password:
        hashed_password = generate_password_hash(password)
        c.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))

    if risk_level:
        c.execute("UPDATE users SET risk=? WHERE username=?", (risk_level, username))

    if fund:
        c.execute("UPDATE users SET fund=? WHERE username=?", (fund, username))

    conn.commit()
    conn.close()

    return jsonify({'message': 'User information updated successfully'}), 200

if __name__ == '__main__':
    app.run()
