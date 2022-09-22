
import pandas as pd
import numpy as np
from src.stock_io import load_stock



def sma(kline, *timeperiod):
    """
    :param kline:
    :param timeperiod:
    :return:
    """
    close = kline[:, 2].astype(np.float)
    return [_sma(close, timeperiod=i) for i in timeperiod]


def _sma(nparr, timeperiod):
    return np.convolve(np.ones(timeperiod) / timeperiod,  nparr)[timeperiod - 1 : -timeperiod + 1]

def max_zf(kline):
    """
    计算最大涨跌幅
    :param kline:
    :return:
    """
    high = kline['high'].astype('float')
    low = kline['low'].astype('float')
    diff = high - low
    return (diff / low * 100).round(2)

def red_bar(kline):
    """
    计算最大涨跌幅
    :param kline:
    :return:
    """
    open = kline['open'].astype('float')
    close = kline['close'].astype('float')
    low = kline['low'].astype('float')
    diff = close - low
    return (diff / low * 100).round(2)



if __name__=='__main__':
    print(red_bar(load_stock('600000')))