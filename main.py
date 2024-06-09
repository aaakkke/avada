from flask import Flask,request,jsonify
from flask_cors import CORS
import akshare as akshare
import pandas as pd
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
CORS(app)


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

@app.route('/strategy_list',methods=['POST'])
def strategy_list():
    data = request.get_json()
    username = data.get('name')
    query = "SELECT risk FROM users WHERE username = %s"
    mysql_cursor.execute(query, (username,))
    risk_level = mysql_cursor.fetchone()[0] 
    print(risk_level)  
    list = [ ]
    dict1 = { }
    dict2 = { }
    if risk_level == "(1,)":       
        dict1['name']='市场中性策略'
        dict1['attribute']=['低风险','低回报']
        dict1['state']=False
        list.append(dict1)        
        dict2['name']='均值回归策略'
        dict2['attribute']=['中低风险','高回报'] #翻了9倍哈哈哈哈哈
        dict2['state']=False
        list.append(dict2)
        dict2 = { }
        dict2['name']='T+0策略'
        dict2['attribute']=['中高风险','中高回报']
        dict2['state']=False
        list.append(dict2)
        dict2 = { }
        dict2['name']='冰山策略'
        dict2['attribute']=['高风险','高回报']
        dict2['state']=False
        list.append(dict2)
    elif risk_level == 2:
        dict1['name']='均值回归策略'
        dict1['attribute']=['中低风险','高回报'] #翻了9倍哈哈哈哈哈
        dict1['state']=False
        list.append(dict1)
        dict2['name']='市场中性策略'
        dict2['attribute']=['低风险','低回报']
        dict2['state']=False              
        list.append(dict2)
        dict2 = { }
        dict2['name']='T+0策略'
        dict2['attribute']=['中高风险','中高回报']
        dict2['state']=False
        list.append(dict2)
        dict2 = { }
        dict2['name']='冰山策略'
        dict2['attribute']=['高风险','高回报']
        dict2['state']=False
        list.append(dict2)
    elif risk_level == 3:
        dict2['name']='市场中性策略'
        dict2['attribute']=['低风险','低回报']
        dict2['state']=False              
        list.append(dict2)
        dict2 = { }
        dict2['name']='均值回归策略'
        dict2['attribute']=['中低风险','高回报'] #翻了9倍哈哈哈哈哈
        dict2['state']=False
        list.append(dict2)
        dict2 = { }
        dict2['name']='T+0策略'
        dict2['attribute']=['中高风险','中高回报']
        dict2['state']=False
        list.append(dict2)
        dict2 = { }
        dict2['name']='冰山策略'
        dict2['attribute']=['高风险','高回报']
        dict2['state']=False
        list.append(dict2)
    elif risk_level == 4:
        dict1['name']='T+0策略'
        dict1['attribute']=['中高风险','中高回报']
        dict1['state']=False     
        list.append(dict1)
        dict2['name']='市场中性策略'
        dict2['attribute']=['低风险','低回报']
        dict2['state']=False              
        list.append(dict2)
        dict2 = { }
        dict2['name']='均值回归策略'
        dict2['attribute']=['中低风险','高回报'] #翻了9倍哈哈哈哈哈
        dict2['state']=False
        list.append(dict2)
        dict2 = { }
        dict2['name']='冰山策略'
        dict2['attribute']=['高风险','高回报']
        dict2['state']=False
        list.append(dict2)
    else:
        dict1['name']='冰山策略'
        dict1['attribute']=['高风险','高回报']
        dict1['state']=False    
        list.append(dict1)
        dict2['name']='市场中性策略'
        dict2['attribute']=['低风险','低回报']
        dict2['state']=False              
        list.append(dict2)
        dict2 = { }
        dict2['name']='均值回归策略'
        dict2['attribute']=['中低风险','高回报'] #翻了9倍哈哈哈哈哈
        dict2['state']=False
        list.append(dict2)
        dict2 = { }
        dict2['name']='T+0策略'
        dict2['attribute']=['中高风险','中高回报']
        dict2['state']=False 
        list.append(dict2)
    return jsonify({'strategy_list':list})

@app.route('/stock',methods=['POST'])
def stock():
    post_data=request.get_json()
    type=post_data.get("type")
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
    print(stock_info)
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
    return jsonify({'stock': stock_list})

@app.route('/stock_select',methods=['POST'])
def stock_select():
    post_data=request.get_json()
    type=post_data.get("type") #类型
    code=post_data.get("code") #代码
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
    return jsonify({'stock_select':stock_list}) 


@app.route('/stock_paint',methods=['POST'])
def stock_paint():
    post_data=request.get_json()
    code=post_data.get("code") #代码
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
    return jsonify({'stock_paint':stock_list}) 

@app.route('/strategy',methods=['POST'])
def strategy():
    post_data=request.get_json()
    name=post_data.get("name") #前端告诉策略名称
    if name=='市场中性策略':
        string = '''import numpy as np
import pandas as pd
import yfinance as yf
import statsmodels.api as sm

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
    print('2')
    # 移动平均
    spread = log_returns1 - log_returns2
    spread_mean = spread.rolling(window=lookback_period).mean()
    #使用滚动窗口计算了价差 spread 在同样窗口期内的移动标准差
    spread_std = spread.rolling(window=lookback_period).std()
    print('3')
    # 计算z-score
    z_score = (spread - spread_mean) / spread_std
    
    # 生成交易信号
    entry_signal = z_score < -1.0
    exit_signal = z_score > -0.5
    print(entry_signal)
    return entry_signal, exit_signal

# 主函数
if __name__ == "__main__":
    # 设置参数
    soc1 = 'KO'
    soc2 = 'TCEHY'
    start_date = '2023-01-01'
    end_date = '2023-10-01'
    initial_capital = 100000  # 初始资金
    tickers = [soc1, soc2]  # 选择两只股票
    lookback_period = 20  # 移动平均的窗口大小
    
    # 获取股票数据
    data = get_stock_data(tickers, start_date, end_date)
    stock1 = data[tickers[0]]
    #print(stock1)
    stock2 = data[tickers[1]]
    #print(stock2)
    

    # 执行配对交易策略
    entry_signal, exit_signal = pairs_trading_strategy(stock1, stock2, lookback_period)


     # 执行交易
    capital = initial_capital
    position = 0  # 初始持仓为0

    for i in range(len(entry_signal)):
        if entry_signal[i] and position == 0:  # 如果有买入信号且当前没有持仓
            position = capital / stock1[i]  # 计算购买数量
            capital -= position * stock1[i]  # 更新可用资金
            print(f"买入 {tickers[0]} at {stock1.index[i]}")
        elif exit_signal[i] and position > 0:  # 如果有卖出信号且当前有持仓
            capital += position * stock1[i]  # 卖出股票获得资金
            position = 0  # 更新持仓数量为0
            print(f"卖出 {tickers[0]} at {stock1.index[i]}")

    # 计算最终资产价值
    final_value = capital + position * stock1[-1]
    print(f"最终资产价值: {final_value}")'''
    elif name=='均值回归策略':
        string='''import numpy as np
import pandas as pd
import yfinance as yf

# 下载股票数据
soc = 'AAPL'
ticker = soc  # 苹果公司的股票
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
    elif name=='T+0策略':
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
    list = [ ]
    dict = { }
    dict['code']=string
    list.append(dict)
    return jsonify({'strategy':list})


@app.route('/set_parameter',methods=['POST'])
def set_parameter():
    post_data=request.get_json()
    parameter=post_data.get("parameter") #参数以字典形式呈现
    #在数据库里存储股票和参数
    
    return "设置成功"

@app.route('/strategy_trade',methods=['POST'])
def strategy_trade():
    #获取股票代信息
    #计算从上次设置策略到现在进行的交易
    #存储交易记录、交易股票和交易金额
    return jsonify({'trade':trade_history})

@app.route('/hand_trade',methods=['POST'])
def hand_trade():
    post_data=request.get_json()
    code=post_data.get("code") #参数以字典形式呈现
    #获取实时价格price
    num=post_data.get("num")
    amount=num*price
    return jsonify({'trade':trade_history})

@app.route('/confirm',methods=['POST'])
def confirm():
    post_data=request.get_json()
    #返回第1个策略的名字和状态
    name0=post_data[0].get("name")
    state0=post_data[0].get("state")
    #返回第2个策略的名字和状态
    name1=post_data[1].get("name")
    state1=post_data[1].get("state")
    #返回第3个策略的名字和状态
    name2=post_data[2].get("name")
    state2=post_data[2].get("state")
    #返回第4个策略的名字和状态
    name3=post_data[3].get("name")
    state3=post_data[3].get("state")
    
    #修改用户这个策略的状态
    
    
    return "已确认"