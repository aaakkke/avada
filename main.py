from flask import Flask,request,jsonify
from flask_cors import CORS
import akshare as akshare
import pandas as pd

app = Flask(__name__)
CORS(app)

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
            stock_list.append(stock_dict)
    print(stock_list)
    return jsonify({'stock_paint':stock_list}) 