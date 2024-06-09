import numpy as np
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
print("现金",cash)

#list = [ ]
#dict = { }
#dict['code']=string
#dict['total_fund']=10000
#dict['soc'] = 'AAPL'
#dict['start_date'] = '2023-01-01'
#dict['end_date'] = '2023-10-01'
#list.append(dict)