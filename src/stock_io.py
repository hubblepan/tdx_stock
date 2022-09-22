# -*- coding:utf-8 -*-
from struct import unpack
import os
import pandas as pd
import numpy as np

dir_day_sh = 'C:\\new_tdx\\vipdoc\\sh\\lday\\'
dir_day_sz = 'C:\\new_tdx\\vipdoc\\sz\\lday\\'


def load_stock(code, plate='sh'):
    try:
        if plate == 'sh':
            ofile = open(dir_day_sh + 'sh' + code + '.day', 'rb')
        elif plate == 'sz':
            ofile = open(dir_day_sz + 'sz' + code + '.day', 'rb')
    except Exception as e:
        print(plate, code, 'not exist')
        return
    buf = ofile.read()
    ofile.close()
    num = len(buf)
    no = num / 32
    b = 0
    e = 32
    items = list()
    index = []
    # [code, dd, str(openPrice), str(high), str(low), str(close), str(ratio), str(amount), str(vol)]
    columns = ['code', 'dd', 'open', 'high', 'low', 'close', 'ratio', 'amount', 'vol']
    for i in range(int(no)):
        a = unpack('IIIIIfII', buf[b:e])
        year = int(a[0] / 10000);
        m = int((a[0] % 10000) / 100);
        month = str(m);
        if m < 10:
            month = "0" + month;
        d = (a[0] % 10000) % 100;
        day = str(d);
        if d < 10:
            day = "0" + str(d);
        dd = str(year) + "-" + month + "-" + day
        openPrice = a[1] / 100.0
        high = a[2] / 100.0
        low = a[3] / 100.0
        close = a[4] / 100.0
        amount = a[5] / 10.0
        vol = a[6]
        unused = a[7]
        if i == 0:
            preClose = close
        ratio = round((close - preClose) / preClose * 100, 2)
        preClose = close
        item = [code, dd, str(openPrice), str(high), str(low), str(close), str(ratio), str(amount), str(vol)]
        index.append(dd)
        items.append(item)
        b = b + 32
        e = e + 32
    return pd.DataFrame(items, index=index, columns=columns)


def get_stock_code_list(dir):
    code_list = []
    for main_dir, sub_dir, file_name_list in os.walk(dir):
        print(main_dir)
        print(sub_dir)
        for file_name in file_name_list:
            code = file_name[2:-4]
            if code[0] in ['6', '0', '3']:
                code_list.append(code)
    return code_list


def load_zxg():
    result = []
    with open('C:\\new_tdx\\T0002\\blocknew\\ZXG.blk', mode='r') as f:
        for line in f.readlines():
            if not '\n' == line and line != '':
                result.append(line[1:])
    return  result


def remove_duplicate_zxg(path = 'C:\\new_tdx\\T0002\\blocknew\\ZXG.blk'):
    result = []
    with open(path, mode='r') as f:
        for line in f.readlines():
            if not '\n' == line and line != '':
                if line.strip('\n') not in result:
                    result.append(line.strip('\n'))
    with open(path, mode='w') as f:
        for stock_code in result:
            f.write(stock_code)
            f.write('\n')
    return  result

# #get_stock_code_list('C:\\new_tdx\\vipdoc\\sh\\lday')

#kline = load_stock('300003', plate='sz')
#print(kline)
# vol = kline['vol'].astype('float').loc['2019-08-09': '2019-08-14']
# print(vol)
# print(vol.max())
# print(type(vol))
# print(type(vol[-1]))
# print(vol[-1])





