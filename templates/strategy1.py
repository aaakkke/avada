import numpy as np
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
    print(f"最终资产价值: {final_value}")

#list = [ ]
#dict = { }
#dict['code']=string
#dict['total_fund']=10000
#dict['soc1'] = 'KO'
#dict['soc2'] = 'TCEHY'
#dict['start_date'] = '2023-01-01'
#dict['end_date'] = '2023-10-01'
#list.append(dict)