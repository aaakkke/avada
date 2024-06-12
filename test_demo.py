import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import pandas as pd
import yfinance as yf
import akshare as akshare
import datetime
# 连接到MySQL数据库
# 填写数据库连接信息
host = '192.168.179.218'
port = 3306  # 根据实际情况修改
database = 'user'
user = 'root'
password = 'Zhangke123'

# 建立数据库连接
mysql_conn = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)

# 创建游标对象
mysql_cursor = mysql_conn.cursor()
# 创建数据库
mysql_cursor.execute("CREATE DATABASE IF NOT EXISTS user")
mysql_conn.commit()
# 切换到用户数据库
mysql_cursor.execute("USE user")
#创建用户策略表
mysql_cursor.execute("CREATE TABLE IF NOT EXISTS user_strategy (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, 市场中性策略 INT, 均值回归策略 INT, T0策略 INT, 冰山策略 INT)")
mysql_conn.commit()

# 创建用户表
mysql_cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, risk INT, ifund FLOAT, fund FLOAT)")
mysql_conn.commit()
#创建交易记录表
mysql_cursor.execute("CREATE TABLE IF NOT EXISTS trade_records (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) NOT NULL, oprate VARCHAR(255) NOT NULL, time VARCHAR(255) NOT NULL, stock_code VARCHAR(255) NOT NULL, stock_name VARCHAR(255) NOT NULL, value FLOAT)")
mysql_conn.commit()

now_username = 'kkkeee'
mysql_cursor.execute("SELECT * FROM user_strategy WHERE username = %s", (now_username,))
result = mysql_cursor.fetchone()
if not result:
    mysql_cursor.execute("INSERT INTO user_strategy (username, 市场中性策略, 均值回归策略, T0策略, 冰山策略) VALUES (%s, %s, %s, %s, %s)", (now_username, 0, 0, 0, 0))
mysql_conn.commit()

#市场中性策略
def pairs_trading(stock1_symbol, stock2_symbol, start_date, end_date, initial_capital):
    # 获取股票数据
    print(type(start_date))
    def get_stock_data(ticker, start, end):
        data = yf.download(ticker, start=start, end=end, progress=False)['Adj Close']
        return data

    # 计算对数收益率
    def calculate_log_returns(data):
        log_returns = np.log(data / data.shift(1))
        return log_returns

    # 执行配对交易策略
    def pairs_trading_strategy(stock1, stock2, lookback_period):
        # 计算对数收益率
        log_returns1 = calculate_log_returns(stock1)
        log_returns2 = calculate_log_returns(stock2)

        # 移动平均
        spread = log_returns1 - log_returns2
        spread_mean = spread.rolling(window=lookback_period).mean()
        spread_std = spread.rolling(window=lookback_period).std()

        # 计算z-score
        z_score = (spread - spread_mean) / spread_std

        # 生成交易信号
        entry_signal = z_score < -1.0
        exit_signal = z_score > -0.5

        return entry_signal, exit_signal

    # 获取股票数据
    stock1_data = get_stock_data(stock1_symbol, start_date, end_date)
    stock2_data = get_stock_data(stock2_symbol, start_date, end_date)

    # 执行配对交易策略
    lookback_period = 20  # 移动平均的窗口大小
    entry_signal, exit_signal = pairs_trading_strategy(stock1_data, stock2_data, lookback_period)

    # 执行交易
    capital = initial_capital
    position_stock1 = 0  # 初始股票1持仓为0
    position_stock2 = 0  # 初始股票2持仓为0

    for i in range(len(entry_signal)):
        if entry_signal[i] and position_stock1 == 0 and position_stock2 == 0:  # 如果有买入信号且当前没有持仓
            # 根据资金分配比例计算买入数量
            allocation_stock1 = capital / 2 / stock1_data[i]
            allocation_stock2 = capital / 2 / stock2_data[i]
            # 更新持仓和可用资金
            position_stock1 += allocation_stock1
            position_stock2 += allocation_stock2
            fund1 = allocation_stock1 * stock1_data[i]
            fund2 = allocation_stock2 * stock2_data[i]
            capital -= fund1
            capital -= fund2
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',stock1_data.index[i],stock1_symbol,yf.Ticker(stock1_symbol).info['longName'],fund1))
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',stock2_data.index[i],stock2_symbol,yf.Ticker(stock2_symbol).info['longName'],fund2))
            mysql_conn.commit()
            #在用户信息表中更新其资产
            mysql_cursor.execute("UPDATE users SET fund=fund-%s WHERE username=%s",(fund1,now_username))
            mysql_cursor.execute("UPDATE users SET fund=fund-%s WHERE username=%s",(fund2,now_username))
            mysql_conn.commit()
            print(f"买入 {stock1_symbol} at {stock1_data.index[i]}，买入 {stock2_symbol} at {stock2_data.index[i]}")
        elif exit_signal[i] and (position_stock1 > 0 or position_stock2 > 0):  # 如果有卖出信号且当前有持仓
            # 卖出所有持仓
            fund1 = position_stock1 * stock1_data[i]
            fund2 = position_stock2 * stock2_data[i]
            capital += fund1
            capital += fund2
            position_stock1 = 0
            position_stock2 = 0
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'卖出',stock1_data.index[i],stock1_symbol,yf.Ticker(stock1_symbol).info['longName'],fund1))
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'卖出',stock2_data.index[i],stock2_symbol,yf.Ticker(stock2_symbol).info['longName'],fund2))
            mysql_conn.commit()
            #在用户信息表中更新其资产
            mysql_cursor.execute("UPDATE users SET fund=fund+%s WHERE username=%s",(fund1,now_username))
            mysql_cursor.execute("UPDATE users SET fund=fund+%s WHERE username=%s",(fund2,now_username))
            mysql_conn.commit()
            print(f"卖出 {stock1_symbol} at {stock1_data.index[i]}，卖出 {stock2_symbol} at {stock2_data.index[i]}")

    # 计算最终资产价值
    final_value = capital + position_stock1 * stock1_data[-1] + position_stock2 * stock2_data[-1]
    print(f"最终资产价值: {final_value}")

#均值回归策略
def mean_reversion(soc, start, end, fund):
    # 下载股票数据
    #soc = '600036.SS'
    ticker = soc
    stock_name = yf.Ticker(soc).info['longName']
    start_date = start
    end_date = end
    initial_capital = fund  # 初始资金
    data = yf.download(ticker, start=start_date, end=end_date)

    # 计算移动平均
    window = 20
    data['RollingMean'] = data['Close'].rolling(window=window).mean()

    # 生成交易信号
    data['BuySignal'] = np.where(data['Close'] < data['RollingMean'], 1, 0)  # 当价格低于移动平均时买入
    data['SellSignal'] = np.where(data['Close'] > data['RollingMean'], 1, 0)  # 当价格高于移动平均时卖出

    position_size = initial_capital // data['Close'][0]  # 根据初始资金计算初始头寸大小

    # 模拟交易
    cash = initial_capital  # 初始现金
    holdings = 0  # 初始持仓
    for i in range(len(data)):
        if data['BuySignal'].iloc[i] == 1 and cash >= data['Close'].iloc[i]:  # 买入信号且有足够现金
            holdings += position_size
            deal_fund = position_size * data['Close'].iloc[i]
            cash -= deal_fund
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',data.index[i],soc,yf,stock_name,deal_fund))
            mysql_conn.commit()
            #在用户信息表中更新其资产
            mysql_cursor.execute("UPDATE users SET fund=fund-%s WHERE username=%s",(deal_fund,now_username))
            mysql_conn.commit()
            print("买入:", data.index[i], "价格:", data['Close'].iloc[i], "持有:", holdings, "现金:", cash,"时间：", data.index[i])
        elif data['SellSignal'].iloc[i] == 1 and holdings > 0:  # 卖出信号且有持仓
            deal_fund = position_size * data['Close'].iloc[i]
            cash += deal_fund
            holdings -= position_size
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'卖出',data.index[i],soc,yf,stock_name,deal_fund))
            mysql_conn.commit()
            #在用户信息表中更新其资产
            mysql_cursor.execute("UPDATE users SET fund=fund+%s WHERE username=%s",(deal_fund,now_username))
            mysql_conn.commit()
            print("卖出:", data.index[i], "价格:", data['Close'].iloc[i], "持有:", holdings, "现金:", cash,"时间：",data.index[i])
    print("现金",cash)


#冰山策略
def ice_mountain(number,code,once_num,price1,price2,start_time,end_time):
    #总交易手数，每次交易手数，高于price1卖出，交易股票代码,开始时间,结束时间
    name='0'
    time='0'
    i=0
    stock_info = akshare.stock_zh_a_hist(symbol=str(code),start_date=start_time,end_date=end_time)
    stock_data=akshare.stock_zh_a_spot_em()
    for index,row in stock_data.iterrows():
        if str(code)==row['代码']:
            name=row['名称']
    number2=0 
    temp_amount=0 #交易金额初始化
    print(stock_info)
    for index, row in stock_info.iterrows(): #遍历历史数据
        price=row['收盘']
        time=row['日期']
        #生成交易（买入）记录
        if number-once_num>=0 and price<price1: #分批购买股票
            temp_amount-=price*once_num
            number-=once_num
            number2+=once_num
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',str(time),str(code),str(name),price*once_num))
            mysql_conn.commit()
            mysql_cursor.execute("UPDATE users SET fund=fund-%s WHERE username=%s",(price*once_num,now_username))
            mysql_conn.commit()
            print(number)
            print(temp_amount)
        elif number-once_num<0 and number>0 and price<price1:
            temp_amount-=price*(number-once_num)
            number=0
            number2+=once_num
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',str(time),str(code),str(name),price*(number-once_num)))
            mysql_conn.commit()
            mysql_cursor.execute("UPDATE users SET fund=fund-%s WHERE username=%s",(price*(number-once_num),now_username))
            mysql_conn.commit()
            print(temp_amount)
        elif price>price2 and number2>0:    #卖出股票
            temp_amount+=price*number2 
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'卖出',str(time),str(code),str(name),price*number2))
            mysql_conn.commit()
            mysql_cursor.execute("UPDATE users SET fund=fund+%s WHERE username=%s",(price*number2,now_username))
            mysql_conn.commit()
            number2=0     
            print(temp_amount)
    

#T0策略
def T_plus_0(initial_funds,code,once_num,start_time,end_time):
    name='0'
    time=[]
    stock_data=akshare.stock_zh_a_spot_em()
    for index,row in stock_data.iterrows():
        if str(code)==row['代码']:
            name=row['名称']
    list=[]
    stock_data = akshare.stock_zh_a_hist(symbol=str(code),period='daily',start_date=start_time,end_date=end_time)
    print(stock_data)
    for index, row in stock_data.iterrows():
        list.append(row["收盘"])
        time.append(row["日期"])
    buy_signals = []
    sell_signals = []
    
    position = 0 
    
    for i in range(1, len(list)):
        # 如果当天收盘价高于前一天收盘价，且当前没有持仓，则买入
        if list[i] < list[i - 1] and position==0:
            print("买入")
            buy_signals.append([code,list[i-1],once_num])
            sell_signals.append(None)
            position += once_num
            initial_funds -= list[i-1] * once_num   # 假设每次买入100股
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',str(time[i]),str(code),str(name),list[i-1] * once_num))
            mysql_conn.commit()
            mysql_cursor.execute("UPDATE users SET fund=fund-%s WHERE username=%s",(list[i-1] * once_num,now_username))
            mysql_conn.commit()
            print(initial_funds)
        # 如果当天收盘价低于前一天收盘价，且当前有持仓，则卖出
        elif list[i] > list[i - 1] and position!=0:
            print("卖出")
            buy_signals.append(None)
            sell_signals.append([code,list[i],once_num])
            initial_funds += list[i] * position  # 假设每次卖出100股
            position = 0
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'卖出',str(time[i]),str(code),str(name),list[i] * once_num))
            mysql_conn.commit()
            mysql_cursor.execute("UPDATE users SET fund=fund+%s WHERE username=%s",(list[i] * once_num,now_username))
            mysql_conn.commit()
            print(initial_funds)
        else:
            buy_signals.append(None)
            sell_signals.append(None)
        
    print("最终资金：", initial_funds)


# 注册用户

def register(username,password,risk_level,fund):
    
    # 检查用户名是否已存在
    mysql_cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    print(111)
    user = mysql_cursor.fetchone()
    print(222)
    if user:
        return 

    # 对密码进行哈希处理后存储
    hashed_password = generate_password_hash(password)
    mysql_cursor.execute("INSERT INTO users (username, password, risk, ifund, fund) VALUES (%s, %s, %s, %s, %s)", (username, hashed_password, risk_level, fund, fund))
    mysql_conn.commit()

    return {'message': 'User registered successfully'}

def test_register():
    assert register('kkkeee','12345678', 1,100000) == {'message': 'Username already exists'}

# 用户登录
def login(username,password):
    # 获取用户信息
    mysql_cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = mysql_cursor.fetchone()

    if user and check_password_hash(user[2], password):  # 检查密码是否匹配
        now_username = username
        # 检查用户是否已存在
        mysql_cursor.execute("SELECT * FROM user_strategy WHERE username = %s", (now_username,))
        result = mysql_cursor.fetchone()
        if not result:
            mysql_cursor.execute("INSERT INTO user_strategy (username, 市场中性策略, 均值回归策略, T0策略, 冰山策略) VALUES (%s, %s, %s, %s, %s)", (now_username, 0, 0, 0, 0))
        else:
            mysql_cursor.execute("UPDATE user_strategy SET 市场中性策略 = %s, 均值回归策略 = %s, T0策略 = %s, 冰山策略 = %s WHERE username = %s", (0, 0, 0, 0, now_username))
        return {'message': 'Login successful'}
    else:
        return {'message': 'Invalid username or password'}

def test_login():
    assert login('kkkeee','12345678') == {'message': 'Login successful'}

# 用户设置
def set(username,password,risk_level,fund):
    
    # 获取用户信息
    mysql_cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = mysql_cursor.fetchone()

    if not user:
        return {'message': 'User not found'}

    # 更新用户信息
    if password:
        hashed_password = generate_password_hash(password)
        mysql_cursor.execute("UPDATE users SET password=%s WHERE username=%s", (hashed_password, username))

    if risk_level:
        mysql_cursor.execute("UPDATE users SET risk=%s WHERE username=%s", (risk_level, username))

    if fund:
        mysql_cursor.execute("UPDATE users SET fund=%s WHERE username=%s", (fund, username))
        mysql_cursor.execute("UPDATE users SET ifund=%s WHERE username=%s", (fund, username))
    mysql_conn.commit()

    return {'message': 'User information updated successfully'}

def test_set():
    assert set('yjw','12345678',2,100000) == {'message': 'User information updated successfully'}

def strategy_list(risk_level):  
    list = [ ]
    dict1 = { }
    dict2 = { }
    if risk_level == 1:       
        dict1['name']='市场中性策略'
        dict1['attribute']=['低风险','低回报']
        mysql_cursor.execute("SELECT 市场中性策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict1['state']=True
        else:
            dict1['state']=False
        list.append(dict1)        
        dict2['name']='均值回归策略'
        dict2['attribute']=['中低风险','高回报']
        mysql_cursor.execute("SELECT 均值回归策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
        dict2 = { }
        dict2['name']='T0策略'
        dict2['attribute']=['中高风险','中高回报']
        mysql_cursor.execute("SELECT T0策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
        dict2 = { }
        dict2['name']='冰山策略'
        dict2['attribute']=['高风险','高回报']
        mysql_cursor.execute("SELECT 冰山策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
    elif risk_level == 2:
        dict1['name']='均值回归策略'
        dict1['attribute']=['中低风险','高回报'] 
        mysql_cursor.execute("SELECT 均值回归策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict1['state']=True
        else:
            dict1['state']=False 
        list.append(dict1)
        dict2['name']='市场中性策略'
        dict2['attribute']=['低风险','低回报']
        mysql_cursor.execute("SELECT 市场中性策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False          
        list.append(dict2)
        dict2 = { }
        dict2['name']='T0策略'
        dict2['attribute']=['中高风险','中高回报']
        mysql_cursor.execute("SELECT T0策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
        dict2 = { }
        dict2['name']='冰山策略'
        dict2['attribute']=['高风险','高回报']
        mysql_cursor.execute("SELECT 冰山策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
    elif risk_level == 3:
        dict1['name']='T0策略'
        dict1['attribute']=['中高风险','中高回报']
        mysql_cursor.execute("SELECT T0策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict1['state']=True
        else:
            dict1['state']=False   
        list.append(dict1)
        dict2['name']='市场中性策略'
        dict2['attribute']=['低风险','低回报']
        mysql_cursor.execute("SELECT 市场中性策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False          
        list.append(dict2)
        dict2 = { }
        dict2['name']='均值回归策略'
        dict2['attribute']=['中低风险','高回报'] 
        mysql_cursor.execute("SELECT 均值回归策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
        dict2 = { }
        dict2['name']='冰山策略'
        dict2['attribute']=['高风险','高回报']
        mysql_cursor.execute("SELECT 冰山策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
    else:
        dict1['name']='冰山策略'
        dict1['attribute']=['高风险','高回报']
        mysql_cursor.execute("SELECT 冰山策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict1['state']=True
        else:
            dict1['state']=False  
        list.append(dict1)
        dict2['name']='市场中性策略'
        dict2['attribute']=['低风险','低回报']
        mysql_cursor.execute("SELECT 市场中性策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False            
        list.append(dict2)
        dict2 = { }
        dict2['name']='均值回归策略'
        dict2['attribute']=['中低风险','高回报'] 
        mysql_cursor.execute("SELECT 均值回归策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
        dict2 = { }
        dict2['name']='T0策略'
        dict2['attribute']=['中高风险','中高回报']
        mysql_cursor.execute("SELECT T0策略 FROM user_strategy WHERE username=%s",(now_username,))
        temp = mysql_cursor.fetchone()[0]
        if temp:
            dict2['state']=True
        else:
            dict2['state']=False 
        list.append(dict2)
    return {'strategy_list':list}

def test_strategy_list():
    assert strategy_list(1) == {'strategy_list': [{'attribute': ['低风险', '低回报'], 'name': '市场中性策略', 'state': True}, {'attribute': ['中低风险', '高回报'], 'name':'均值回归策略','state':True},{'attribute': ['中高风险', '中高回报'], 'name': 'T0策略', 'state': True}, {'attribute': ['高风险', '高回报'], 'name': '冰山策略', 'state': True}]}


def strategy(name):
    if name=='市场中性策略':
        string = '''import numpy as np
import pandas as pd
import yfinance as yf

# 获取股票数据
def get_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Adj Close']
    return data

# 计算股票的对数收益率
def calculate_log_returns(data):
    log_returns = np.log(data / data.shift(1))
    return log_returns

# 执行配对交易策略
def pairs_trading_strategy(stock1, stock2, lookback_period):
    # 计算对数收益率
    log_returns1 = calculate_log_returns(stock1)
    log_returns2 = calculate_log_returns(stock2)

    # 移动平均
    spread = log_returns1 - log_returns2
    spread_mean = spread.rolling(window=lookback_period).mean()
    spread_std = spread.rolling(window=lookback_period).std()

    # 计算z-score
    z_score = (spread - spread_mean) / spread_std
    
    # 生成交易信号
    entry_signal = z_score < -1.0
    exit_signal = z_score > -0.5

    return entry_signal, exit_signal

# 主函数
if __name__ == "__main__":
    # 设置参数
    stock1_symbol = '0700.HK'  # 第一支股票代码
    stock2_symbol = '600036.SS'  # 第二支股票代码
    start_date = '2023-01-01'
    end_date = '2023-10-01'
    initial_capital = 100000  # 初始资金
    lookback_period = 20  # 移动平均的窗口大小
    
    # 获取股票数据
    stock1_data = get_stock_data(stock1_symbol, start_date, end_date)
    stock2_data = get_stock_data(stock2_symbol, start_date, end_date)

    # 执行配对交易策略
    entry_signal, exit_signal = pairs_trading_strategy(stock1_data, stock2_data, lookback_period)

    # 执行交易
    capital = initial_capital
    position_stock1 = 0  # 初始股票1持仓为0
    position_stock2 = 0  # 初始股票2持仓为0

    for i in range(len(entry_signal)):
        if entry_signal[i] and position_stock1 == 0 and position_stock2 == 0:  # 如果有买入信号且当前没有持仓
            # 根据资金分配比例计算买入数量
            allocation_stock1 = capital / 2 / stock1_data[i]
            allocation_stock2 = capital / 2 / stock2_data[i]
            # 更新持仓和可用资金
            position_stock1 += allocation_stock1
            position_stock2 += allocation_stock2
            capital -= allocation_stock1 * stock1_data[i]
            capital -= allocation_stock2 * stock2_data[i]
            print(f"买入 {stock1_symbol} at {stock1_data.index[i]}，买入 {stock2_symbol} at {stock2_data.index[i]}")
        elif exit_signal[i] and (position_stock1 > 0 or position_stock2 > 0):  # 如果有卖出信号且当前有持仓
            # 卖出所有持仓
            capital += position_stock1 * stock1_data[i]
            capital += position_stock2 * stock2_data[i]
            position_stock1 = 0
            position_stock2 = 0
            print(f"卖出 {stock1_symbol} at {stock1_data.index[i]}，卖出 {stock2_symbol} at {stock2_data.index[i]}")

    # 计算最终资产价值
    final_value = capital + position_stock1 * stock1_data[-1] + position_stock2 * stock2_data[-1]
    print(f"最终资产价值: {final_value}")'''
    elif name=='均值回归策略':
        string='''import numpy as np
import pandas as pd
import yfinance as yf

# 下载股票数据
soc = '600036.SS'
ticker = soc  
start_date = '2023-01-01'
end_date = '2023-10-01'
initial_capital = 10000  # 初始资金
data = yf.download(ticker, start=start_date, end=end_date)

# 计算移动平均
window = 20
data['RollingMean'] = data['Close'].rolling(window=window).mean()

# 生成交易信号
data['BuySignal'] = np.where(data['Close'] < data['RollingMean'], 1, 0)  # 当价格低于移动平均时买入
data['SellSignal'] = np.where(data['Close'] > data['RollingMean'], 1, 0)  # 当价格高于移动平均时卖出



position_size = initial_capital // data['Close'][0]  # 根据初始资金计算初始头寸大小

# 模拟交易
cash = initial_capital  # 初始现金
holdings = 0  # 初始持仓
for i in range(len(data)):
    if data['BuySignal'].iloc[i] == 1 and cash >= data['Close'].iloc[i]:  # 买入信号且有足够现金
        holdings += position_size
        cash -= position_size * data['Close'].iloc[i]
    elif data['SellSignal'].iloc[i] == 1 and holdings > 0:  # 卖出信号且有持仓
        cash += position_size * data['Close'].iloc[i]
        holdings -= position_size
# 计算总收益率
total_return = (cash + holdings * data['Close'].iloc[-1] - initial_capital) / initial_capital
print("累计收益率:", total_return)
print("现金",cash)'''
    elif name=='T0策略':
        string='''j=0
for stock_code in code:
    list=[]
    stock_data = akshare.stock_zh_a_hist(symbol=stock_code)
    for index, row in stock_data.iterrows():
        list.append(row["收盘"])
    
    buy_signals = []
    sell_signals = []
    position = False #调用数据库获得是否持仓
    num=once_num[j]
    for i in range(1, len(list)):
        # 如果当天收盘价高于前一天收盘价，且当前没有持仓，则买入
        if list[i] > list[i - 1] and not position:
            buy_signals.append([stock_code,list[i-1],num])
            sell_signals.append(None)
            position = True
            initial_funds -= list[i-1] * num   # 假设每次买入100股
        # 如果当天收盘价低于前一天收盘价，且当前有持仓，则卖出
        if list[i] < list[i - 1] and position:
            buy_signals.append(None)
            sell_signals.append([stock_code,list[i],num])
            position = False
            initial_funds += list[i] * num  # 假设每次卖出100股
        else:
            buy_signals.append(None)
            sell_signals.append(None)
        
    
        stock_data['buy_signals'] = buy_signals
        stock_data['sell_signals'] = sell_signals
        print(stock_data)
        print("最终资金：", initial_funds)
    j+=1'''
    elif name=='冰山策略':
        string='''today=datetime.datetime.now().strftime('%Y%m%d')
stock_info = akshare.stock_zh_a_hist(symbol='600519',period='daily',start_date='20230530',end_date=today)
i=0
number2=[]
for item in code:
    number2[i]=number[i]
    for index, row in stock_info.iterrows():
        if number[i]==0:
            break
        price=row['收盘']
        #生成交易（买入）记录
        if number[i]-once_num[i]>=0:
            temp_amount=price*once_num[i]
            number[i]-=once_num[i]
        elif number[i]-once_num[i]<0 and number[i]!=0:
            temp_amount=price*(number[i]-once_num[i])
            number[i]=0
        if price>price1:    #卖出
            temp_amount=price*(number2[i]-number[i])
    i+=1        
        
print(stock_info)'''
    list = [string]
    return {'strategy':list}

def test_strategy():
    assert strategy('市场中性策略')=={'strategy':['''import numpy as np
import pandas as pd
import yfinance as yf

# 获取股票数据
def get_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Adj Close']
    return data

# 计算股票的对数收益率
def calculate_log_returns(data):
    log_returns = np.log(data / data.shift(1))
    return log_returns

# 执行配对交易策略
def pairs_trading_strategy(stock1, stock2, lookback_period):
    # 计算对数收益率
    log_returns1 = calculate_log_returns(stock1)
    log_returns2 = calculate_log_returns(stock2)

    # 移动平均
    spread = log_returns1 - log_returns2
    spread_mean = spread.rolling(window=lookback_period).mean()
    spread_std = spread.rolling(window=lookback_period).std()

    # 计算z-score
    z_score = (spread - spread_mean) / spread_std
    
    # 生成交易信号
    entry_signal = z_score < -1.0
    exit_signal = z_score > -0.5

    return entry_signal, exit_signal

# 主函数
if __name__ == "__main__":
    # 设置参数
    stock1_symbol = '0700.HK'  # 第一支股票代码
    stock2_symbol = '600036.SS'  # 第二支股票代码
    start_date = '2023-01-01'
    end_date = '2023-10-01'
    initial_capital = 100000  # 初始资金
    lookback_period = 20  # 移动平均的窗口大小
    
    # 获取股票数据
    stock1_data = get_stock_data(stock1_symbol, start_date, end_date)
    stock2_data = get_stock_data(stock2_symbol, start_date, end_date)

    # 执行配对交易策略
    entry_signal, exit_signal = pairs_trading_strategy(stock1_data, stock2_data, lookback_period)

    # 执行交易
    capital = initial_capital
    position_stock1 = 0  # 初始股票1持仓为0
    position_stock2 = 0  # 初始股票2持仓为0

    for i in range(len(entry_signal)):
        if entry_signal[i] and position_stock1 == 0 and position_stock2 == 0:  # 如果有买入信号且当前没有持仓
            # 根据资金分配比例计算买入数量
            allocation_stock1 = capital / 2 / stock1_data[i]
            allocation_stock2 = capital / 2 / stock2_data[i]
            # 更新持仓和可用资金
            position_stock1 += allocation_stock1
            position_stock2 += allocation_stock2
            capital -= allocation_stock1 * stock1_data[i]
            capital -= allocation_stock2 * stock2_data[i]
            print(f"买入 {stock1_symbol} at {stock1_data.index[i]}，买入 {stock2_symbol} at {stock2_data.index[i]}")
        elif exit_signal[i] and (position_stock1 > 0 or position_stock2 > 0):  # 如果有卖出信号且当前有持仓
            # 卖出所有持仓
            capital += position_stock1 * stock1_data[i]
            capital += position_stock2 * stock2_data[i]
            position_stock1 = 0
            position_stock2 = 0
            print(f"卖出 {stock1_symbol} at {stock1_data.index[i]}，卖出 {stock2_symbol} at {stock2_data.index[i]}")

    # 计算最终资产价值
    final_value = capital + position_stock1 * stock1_data[-1] + position_stock2 * stock2_data[-1]
    print(f"最终资产价值: {final_value}")''']}

def confirm(name0,state0,name1,state1,name2,state2,name3,state3):
    #创建用户策略表
    mysql_cursor.execute("CREATE TABLE IF NOT EXISTS user_strategy (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE NOT NULL, 市场中性策略 INT, 均值回归策略 INT, T0策略 INT, 冰山策略 INT)")
    mysql_conn.commit()
    # 检查用户是否已存在
    mysql_cursor.execute("SELECT * FROM user_strategy WHERE username = %s", (now_username,))
    result = mysql_cursor.fetchone()
    if not result:
        mysql_cursor.execute("INSERT INTO user_strategy (username, 市场中性策略, 均值回归策略, T0策略, 冰山策略) VALUES (%s, %s, %s, %s, %s)", (now_username, 0, 0, 0, 0))
    else:
        mysql_cursor.execute("UPDATE user_strategy SET 市场中性策略 = %s, 均值回归策略 = %s, T0策略 = %s, 冰山策略 = %s WHERE username = %s", (0, 0, 0, 0, now_username))
    
    #返回第1个策略的名字和状态
    if state0 == True:
        if name0 == "市场中性策略":
            mysql_cursor.execute("UPDATE user_strategy SET 市场中性策略 = 1 WHERE username = %s", (now_username,))
        elif name0 == "均值回归策略":
            mysql_cursor.execute("UPDATE user_strategy SET 均值回归策略 = 1 WHERE username = %s", (now_username,))
        elif name0 == "T0策略":
            mysql_cursor.execute("UPDATE user_strategy SET T0策略 = 1 WHERE username = %s", (now_username,))
        elif name0 == "冰山策略":
            mysql_cursor.execute("UPDATE user_strategy SET 冰山策略 = 1 WHERE username = %s", (now_username,))
    #返回第2个策略的名字和状态
    if state1 == True:
        if name1 == "市场中性策略":
            mysql_cursor.execute("UPDATE user_strategy SET 市场中性策略 = 1 WHERE username = %s", (now_username,))
        elif name1 == "均值回归策略":
            mysql_cursor.execute("UPDATE user_strategy SET 均值回归策略 = 1 WHERE username = %s", (now_username,))
        elif name1 == "T0策略":
            mysql_cursor.execute("UPDATE user_strategy SET T0策略 = 1 WHERE username = %s", (now_username,))
        elif name1 == "冰山策略":
            mysql_cursor.execute("UPDATE user_strategy SET 冰山策略 = 1 WHERE username = %s", (now_username,))
    #返回第3个策略的名字和状态
    if state2 == True:
        if name2 == "市场中性策略":
            mysql_cursor.execute("UPDATE user_strategy SET 市场中性策略 = 1 WHERE username = %s", (now_username,))
        elif name2 == "均值回归策略":
            mysql_cursor.execute("UPDATE user_strategy SET 均值回归策略 = 1 WHERE username = %s", (now_username,))
        elif name2 == "T0策略":
            mysql_cursor.execute("UPDATE user_strategy SET T0策略 = 1 WHERE username = %s", (now_username,))
        elif name2 == "冰山策略":
            mysql_cursor.execute("UPDATE user_strategy SET 冰山策略 = 1 WHERE username = %s", (now_username,))
    #返回第4个策略的名字和状态
    if state3 == True:
        if name3 == "市场中性策略":
            mysql_cursor.execute("UPDATE user_strategy SET 市场中性策略 = 1 WHERE username = %s", (now_username,))
        elif name3 == "均值回归策略":
            mysql_cursor.execute("UPDATE user_strategy SET 均值回归策略 = 1 WHERE username = %s", (now_username,))
        elif name3 == "T0策略":
            mysql_cursor.execute("UPDATE user_strategy SET T0策略 = 1 WHERE username = %s", (now_username,))
        elif name3 == "冰山策略":
            mysql_cursor.execute("UPDATE user_strategy SET 冰山策略 = 1 WHERE username = %s", (now_username,))
        
    # 提交更改
    mysql_conn.commit()

    return {'message': 'successfully'}

def test_confirm():
    assert confirm("市场中性策略",True,"均值回归策略",True,"T0策略",True,"冰山策略",True) == {'message': 'successfully'}


def user_info():
    mysql_cursor.execute("SELECT * FROM users WHERE username = %s",(now_username,))
    result = mysql_cursor.fetchone()
    dict={
        "用户名":now_username,
        "密码":result[2],
        "风险等级":result[3],
        "初始资金":result[5]
        }
    return {"user_info":dict}
    
def test_user_info():
    {'user_info': {'初始资金': 800425.0, '密码': 'scrypt:32768:8:1$CJuWVf1j44icdux2$65efedc09158c674e2ee7c3f7789437c3adb0a5e51f5d5054f11d58990155cf7eea72cdd180c66110ccc68a29d67129f6500d86cd258564fab1579b1f6fcc835', '用户名': 'kkkeee', '风险等级': 4}}
def deal1(strategy_name):
    para = [ ]
    dict = { }
    if strategy_name == '市场中性策略':
        dict['股票代码1'] = "0700.HK"
        dict['股票代码2'] = "600036.SS"
        dict['开始时间'] = "2023-01-01"
        dict['结束时间'] = "2023-10-01"
        dict['初始资金'] = 100000
        dict['策略名称']='市场中性策略'
    elif strategy_name == '均值回归策略':
        dict['股票代码'] = '600036.SS'
        dict['开始时间'] = "2023-01-01"
        dict['结束时间'] = "2023-10-01"
        dict['初始资金'] = 10000
        dict['策略名称']='均值回归策略'
    elif strategy_name == '冰山策略':
        dict['策略名称']='冰山策略'
        dict['初始资金']=10000
        dict['股票代码'] = '600519'
        dict['开始时间'] = "20220611"
        dict['结束时间'] = "20240611"
        dict['总交易手数']=100
        dict['每次交易手数']=10
        dict['买入价格']=1610
        dict['卖出价格']=1630
    elif strategy_name == 'T0策略':
        dict['策略名称']='T0策略'
        dict['股票代码'] = '600519'
        dict['开始时间'] = "20230511"
        dict['结束时间'] = "20240611"
        dict['初始资金'] = 100000
        dict['每次交易手数']=10
    para.append(dict)
    return {'parameter':para}

def test_deal1_1():
    assert deal1("市场中性策略") == {'parameter':[{
        '股票代码1': "0700.HK",
        '股票代码2': "600036.SS",
        '开始时间': "2023-01-01",
        '结束时间': "2023-10-01",
        '初始资金': 100000,
        '策略名称':'市场中性策略'
    }]}
def test_deal1_2():
    assert deal1("均值回归策略") == {'parameter':[{
        '股票代码': "600036.SS",
        '开始时间': "2023-01-01",
        '结束时间': "2023-10-01",
        '初始资金': 10000,
        '策略名称':'均值回归策略'
    }]}
def test_deal1_3():
    assert deal1("冰山策略") == {'parameter':[{
        '总交易手数':100,
        '每次交易手数':10,
        '买入价格':1610,
        '卖出价格':1630,
        '股票代码': "600519",
        '开始时间': "20220611",
        '结束时间': "20240611",
        '初始资金': 10000,
        '策略名称':'冰山策略'
    }]}    
    
def test_deal1_4():
    assert deal1("T0策略") == {'parameter':[{
        '每次交易手数':10,
        '股票代码': "600519",
        '开始时间': "20230511",
        '结束时间': "20240611",
        '初始资金': 100000,
        '策略名称':'T0策略'
    }]}
    

def submit_strategy(name):
    mysql_cursor.execute("SELECT fund FROM users WHERE username=%s", (now_username,))
    hold_fund = mysql_cursor.fetchone()[0]
    if name['策略名称']=='市场中性策略':
        funds=name["初始资金"]
        start_time=name["开始时间"][:10]
        end_time=name["结束时间"][:10]
        code1=name["股票代码1"]
        code2=name["股票代码2"]
        print(code2)
        if funds>hold_fund:
            return {'error':'Insufficient funds'}
        else:
            pairs_trading(code1, code2, start_time, end_time, funds)
            return {"message":"successfully"}
    
    elif name['策略名称']=='均值回归策略':
        funds=name["初始资金"]
        start_time = name["开始时间"][:10]
        end_time=name["结束时间"][:10]
        code=name["股票代码"]
        if funds>hold_fund:
            return {'error':'Insufficient funds'}
        else:
            mean_reversion(code,start_time,end_time,funds)
            return {"message":"successfully"}
    
    elif name['策略名称']=='冰山策略':
        print('111')
        funds=float(name["初始资金"])
        start_time=name["开始时间"][:10].replace('-', '')
        end_time=name["结束时间"][:10].replace('-', '')
        code=name["股票代码"]
        price1=float(name["买入价格"])
        price2=float(name["卖出价格"])
        number=float(name["总交易手数"]) #总交易手数
        once_num=float(name["每次交易手数"])
        #在数据库里存储股票和参数
        if funds>hold_fund:
            return {'error':'Insufficient funds'}
        else:
            ice_mountain(number,code,once_num,price1,price2,start_time,end_time)
            return {"message":"successfully"}
    elif name['策略名称']=='T0策略':
        start_time=name["开始时间"][:10].replace('-', '')
        end_time=name["结束时间"][:10].replace('-', '')
        
        once_num=float(name["每次交易手数"])
        initial_funds=float(name["初始资金"])
        code=name["股票代码"]

        if initial_funds>hold_fund:
            return {'error':'Insufficient funds'}
        else:
            T_plus_0(initial_funds,code,once_num,start_time,end_time)
            return {"message":"successfully"}
        #在数据库里存储股票和参数
    else:
        code=name["股票代码"] #代码
        num=float(name["总交易手数"]) #购买手数
        sell=name["买入卖出"]
        price=0
        name='0'
        time=datetime.date.today()

        stock_info=akshare.stock_zh_a_spot_em()
        print(stock_info)
        for index, row in stock_info.iterrows():
            if str(code)==row['代码']:
                price=row['最新价']
                name=row['名称']
                amount=num*price #交易金额
        if sell=='买入':
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',str(time),str(code),str(name),amount))
            mysql_conn.commit()
            mysql_cursor.execute("UPDATE users SET fund=fund-%s WHERE username=%s",(amount,now_username))
            mysql_conn.commit()
        elif sell=='卖出':
            mysql_cursor.execute("INSERT INTO trade_records (username, oprate , time, stock_code, stock_name, value) VALUES (%s, %s, %s, %s, %s, %s)",(now_username,'买入',str(time),str(code),str(name),amount))
            mysql_conn.commit()
            mysql_cursor.execute("UPDATE users SET fund=fund+%s WHERE username=%s",(amount,now_username))
            mysql_conn.commit()
        return {"message":"successfully"}    

def test_submit_strategy_1():
    dict={'策略名称':'冰山策略',"初始资金":10000,"开始时间":"20220611","结束时间":"20240611","股票代码":"600519",'总交易手数':100,'每次交易手数':10,'买入价格':1610,'卖出价格':1630}
    assert submit_strategy(dict) == {"message":"successfully"}

def test_submit_strategy_2(): #无策略交易
    dict={'策略名称':None,"股票代码":"600519",'总交易手数':100,'买入卖出':'买入'}
    assert submit_strategy(dict) == {"message":"successfully"}

def asset_info():
    mysql_cursor.execute("SELECT ifund FROM users WHERE username = %s",(now_username,))
    total_assets=mysql_cursor.fetchone()[0] #总资产
    mysql_cursor.execute("SELECT fund FROM users WHERE username = %s",(now_username,))
    current_assets=mysql_cursor.fetchone()[0] #可用资产
    mysql_cursor.execute("SELECT * FROM trade_records WHERE username = %s",(now_username,))
    msg = mysql_cursor.fetchall()
    transaction=[ ] 
    for tran in msg:
        dict = { }
        dict['交易时间'] = tran[3][:10]
        dict['股票代码'] = tran[4]
        dict['股票名称'] = tran[5]
        dict['交易金额'] = tran[6]
        dict['交易类型'] = tran[2]
        transaction.append(dict)
    return {"message":"successfully"}

def test_asset_info(): 
    assert asset_info() == {"message":"successfully"}
    
def stock(type):
    print('type',type)
    stock_info = pd.DataFrame()  # 设置默认值为一个空的DataFrame
    if type == "sh":  # 沪市
        stock_info = akshare.stock_sh_a_spot_em()
    elif type == "sz":  # 深市
        stock_info = akshare.stock_sz_a_spot_em()
    elif type == "cy":  # 创业板
        stock_info = akshare.stock_cy_a_spot_em()
    elif type == "kc":  # 科创板
        stock_info = akshare.stock_kc_a_spot_em()
    # 将每支股票信息转化为字典形式，并放入一个列表中
    stock_list = []
    if not stock_info.empty:  # 确保DataFrame不为空
        for index, row in stock_info.iterrows():
            stock_dict = {
                '股票代码': str(row['代码']),
                '名称': str(row['名称']),
                '最新价': str(row['最新价']),
                '涨跌幅': str(row['涨跌幅']),
                '涨跌额': str(row['涨跌额']),
                '成交量': str(row['成交量']),
                '成交额': str(row['成交额']),
                '振幅': str(row['振幅']),
                '最高价': str(row['最高']),
                '最低价': str(row['最低']),
                '今开': str(row['今开']),
                '昨收': str(row['昨收']),
                '量比': str(row['量比']),
                '换手率': str(row['换手率'])
            }
            stock_list.append(stock_dict)

    print(stock_list)
    return {"message":"successfully"}

def test_stock(): 
    assert stock("sh") == {"message":"successfully"}

def stock_select(type,code):
    if type=="sh":  #沪市
        stock_info = akshare.stock_sh_a_spot_em()
    if type=="sz":  #深市
        stock_info = akshare.stock_sz_a_spot_em()
    if type=="cy":  #创业板
        stock_info = akshare.stock_cy_a_spot_em()
    if type=="kc":  #科创板
        stock_info = akshare.stock_kc_a_spot_em()
    stock_list=[]
    for index, row in stock_info.iterrows():
        if code==row['代码']:
            stock_dict = {
                '序号':str(row['序号']),
                '股票代码': str(row['代码']),
                '名称': str(row['名称']),
                '最新价': str(row['最新价']),
                '涨跌幅': str(row['涨跌幅']),
                '涨跌额': str(row['涨跌额']),
                '成交量': str(row['成交量']),
                '成交额': str(row['成交额']),
                '振幅': str(row['振幅']),
                '最高价': str(row['最高']),
                '最低价': str(row['最低']),
                '今开': str(row['今开']),
                '昨收': str(row['昨收']),
                '量比': str(row['量比']),
                '换手率': str(row['换手率'])
            }
            stock_list.append(stock_dict)
            break

    print(stock_list)
    return {'stock_select':stock_list} 

def test_stock_select(): 
    assert stock_select("sh","600519") == {'stock_select':[{
            "今开": "1570.0",
            "名称": "贵州茅台",
            "序号": "1518",
            "成交量": "33171.0",
            "成交额": "5230086503.0",
            "振幅": "1.27",
            "换手率": "0.26",
            "昨收": "1569.0",
            "最低价": "1570.0",
            "最新价": "1571.68",
            "最高价": "1590.0",
            "涨跌幅": "0.17",
            "涨跌额": "2.68",
            "股票代码": "600519",
            "量比": "0.98"
        }]}

def stock_paint(code):
    stock_info = akshare.stock_zh_a_hist(symbol=code,period='daily',start_date='20230530',end_date='20240530')
    stock_list=[]
    i=1
    for index, row in stock_info.iterrows():
        if code==row['股票代码']:
            stock_dict = {
                '日期': str(row['日期']),
                '成交量': str(row['成交量']),
                '成交额': str(row['成交额']),
                '最高价': str(row['最高']),
                '最低价': str(row['最低']),
                '今开': str(row['开盘']),
                '昨收': str(row['收盘']),
            }
            if i%3==1:
                stock_list.append(stock_dict)
            i+=1
    print(stock_list)
    return {"message":"successfully"}

def test_stock_paint(): 
    assert stock_paint("600519")=={"message":"successfully"}