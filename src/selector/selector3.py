# -*- coding:utf-8 -*-
import src.stock_io as sio
from src.StockIndicator import max_zf, _sma
import numpy as np
from src.terminate import remove_duplicate_zxg

def main(position=-1, plate='sh'):
    if plate == 'sh':
        code_list = sio.get_stock_code_list(sio.dir_day_sh)
    elif plate == 'sz':
        code_list = sio.get_stock_code_list(sio.dir_day_sz)
    else:
        print('error: plate parameter error')
        return
    print('aaa', code_list)
    result = []
    for stock_code in code_list:
        try:
            if stock_code == '600129':
                print(stock_code)
            kline = sio.load_stock(stock_code, plate=plate)
            s_vol = kline['vol'][position - 1: ].astype('float')[position]
            s_amount = kline['amount'][position - 1: ].astype('float')[position]
            s_ratio = kline['ratio'][position - 1: ].astype('float')[position]
            s_open = kline['open'][position - 1: ].astype('float')[position]
            s_high = kline['high'][position - 1: ].astype('float')[position]
            s_low = kline['low'][position - 1: ].astype('float')[position]
            s_close = kline['close'][position - 1: ].astype('float')[position]

            s_close_5 = kline['close'][position - 5: position].astype('float')
            sma_close_5 = _sma(np.array(kline['close'].astype('float')), 5)[position - 9:]
            sma_close_10 = _sma(np.array(kline['close'].astype('float')), 10)[position - 9:]
            sma_close_20 = _sma(np.array(kline['close'].astype('float')), 20)[position - 9:]
            sma_vol_10 = _sma(np.array(kline['vol'].astype('float')), 10)[position - 9:]
            sma_vol_20 = _sma(np.array(kline['vol'].astype('float')), 20)[position - 9:]
            vol = kline['vol'][position - 9: ].astype('float')
            # 成交额要大于1.5亿
            if s_amount * 10 < 1 * 100000000:
                continue

            # 开盘价要小于于收盘价
            if s_open > s_close:
                continue

            s_zf = (s_high - s_low) / s_low * 100
            s_entity = (s_close - s_open) / s_open * 100
            s_max = (s_close - s_low) / s_low * 100

            # 不考虑40元以上的股票
            if sma_close_5[position] > 50:
                continue

            # 不考虑没有波动的股票
            if s_entity < 4:
                continue

            # 若上涨幅度没有超过前面两个k线的高度， 不考虑
            if s_close <= np.max(s_close_5):
                continue
            # if s_high[position] < np.max(s_close[position + 1: position + 3]):
            #     return False

            # 突然爆量的涨幅不要
            # if s_vol[position] / s_vol[position + 1] > 1.5:
            #     return False

            if vol[position] / max(sma_vol_10[position], sma_vol_20[position]) > 1.3:
                continue

            # 没有穿过均线的不要
            if s_low > max(sma_close_10[position], sma_close_10[position], sma_close_20[position]):
                continue
            # if s_high < min(sma_close_20[position], sma_close_20[position]):
            #     continue
            # if s_high < sma_close_10[position] < sma_close_20[position]:
            #     continue
            result.append(stock_code)
            print(stock_code)
        except Exception as e:
            print(111, e)
            pass

    print(len(result))
    return result
    # with open('C:\\new_tdx\T0002\\blocknew\\ZXG.blk', mode='a') as f:
    #     for stock_code in result:
    #         if stock_code[0] == '6':
    #             f.write('1'+stock_code)
    #         else:
    #             f.write('0' + stock_code)
    #         f.write('\n')


if __name__=='__main__':
    result = []
    for index in [-2]:
        result += main(index, plate='sh')
        result += main(index, plate='sz')
    with open('tod.txt', mode='w') as f:
        for item in result:
            f.write(item)
            f.write('\n')
    # remove_duplicate_zxg()


