from flask import Flask,request,jsonify
#from flask_cors import CORS
import akshare as akshare

app = Flask(__name__)
#CORS(app,resources=r'/*')

@app.route('/stock',methods=['POST'])
def stock():
    type=request.form.get("type")
    if type=="sh":  #沪市
        stock_info = akshare.stock_sh_a_spot_em()
    if type=="sz":  #深市
        stock_info = akshare.stock_sz_a_spot_em()
    if type=="cy":  #创业板
        stock_info = akshare.stock_cy_a_spot_em()
    if type=="kc":  #科创板
        stock_info = akshare.stock_kc_a_spot_em()
    # 将每支股票信息转化为字典形式，并放入一个列表中
    stock_list = []
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
    return jsonify(stock_list)

@app.route('/stock_select',methods=['POST'])
def stock_select():
    code=request.form.get("code")
    type=request.form.get("type")
    if type=="sh":  #沪市
        stock_info = akshare.stock_sh_a_spot_em()
    if type=="sz":  #深市
        stock_info = akshare.stock_sz_a_spot_em()
    if type=="cy":  #创业板
        stock_info = akshare.stock_cy_a_spot_em()
    if type=="kc":  #科创板
        stock_info = akshare.stock_kc_a_spot_em()
        
    stock_dict={}
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

    print(stock_dict)
    return jsonify(stock_dict) 


@app.route('/stock_paint',methods=['POST'])
def stock_paint():
    code=request.form.get("code")
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
    return jsonify(stock_list)